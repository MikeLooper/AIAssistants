import json

import pytest

from comp_review_api.config import DEFAULT_REVIEWER_ROOT, Settings, SettingsError, load_settings


def test_defaults():
    s = Settings().validate()
    assert s.environment == "development"
    assert s.port == 12001
    assert s.default_tool == "auto"
    assert not s.is_production
    assert s.root == DEFAULT_REVIEWER_ROOT
    assert s.reviewer_script == DEFAULT_REVIEWER_ROOT / "scripts" / "run_review.py"
    assert s.tests_dir == DEFAULT_REVIEWER_ROOT / "test" / "logic"


def test_bundled_appsettings_file_loads():
    s = load_settings(env={})
    assert s.port == 12001
    assert s.environment in ("development", "production")


def test_json_file_uses_pascal_case_keys(tmp_path):
    f = tmp_path / "s.json"
    f.write_text(json.dumps({"$comment": "ignored", "Environment": "Production", "Port": 13000,
                             "DefaultModel": "claude-sonnet-5-5", "MaxConcurrentJobs": 3,
                             "AvailableModels": {"Claude": ["a"]}, "KeepSources": True}))
    s = load_settings(f, env={})
    assert s.environment == "production" and s.is_production
    assert s.port == 13000
    assert s.default_model == "claude-sonnet-5-5"
    assert s.max_concurrent_jobs == 3
    assert s.available_models == {"claude": ["a"]}
    assert s.keep_sources is True


def test_environment_variables_override_the_file(tmp_path):
    f = tmp_path / "s.json"
    f.write_text(json.dumps({"Environment": "development", "Port": 13000}))
    env = {"COMP_REVIEW_API_ENVIRONMENT": "production", "COMP_REVIEW_API_PORT": "14000",
           "COMP_REVIEW_API_CORS_ORIGINS": "http://a, http://b", "COMP_REVIEW_API_KEEP_SOURCES": "yes",
           "COMP_REVIEW_API_AVAILABLE_MODELS": '{"copilot": ["gpt-5"]}', "COMP_REVIEW_API_DEFAULT_MODEL": ""}
    s = load_settings(f, env=env)
    assert s.environment == "production"
    assert s.port == 14000
    assert s.cors_origins == ["http://a", "http://b"]
    assert s.keep_sources is True
    assert s.available_models == {"copilot": ["gpt-5"]}
    assert s.default_model is None


def test_config_path_from_environment(tmp_path):
    f = tmp_path / "other.json"
    f.write_text(json.dumps({"Port": 15000}))
    assert load_settings(env={"COMP_REVIEW_API_CONFIG": str(f)}).port == 15000


@pytest.mark.parametrize("content, message", [
    ({"Environment": "staging"}, "Environment"),
    ({"DefaultTool": "gemini"}, "DefaultTool"),
    ({"Port": 70000}, "Port"),
    ({"MaxUploadMb": 0}, "MaxUploadMb"),
    ({"Bogus": 1}, "unknown setting"),
    ({"Port": "abc"}, "integer"),
    ({"KeepSources": "maybe"}, "true or false"),
    ({"DefaultModel": "--evil"}, "invalid model"),
    ({"AvailableModels": ["x"]}, "object"),
])
def test_invalid_values_are_rejected(tmp_path, content, message):
    f = tmp_path / "s.json"
    f.write_text(json.dumps(content))
    with pytest.raises(SettingsError, match=message):
        load_settings(f, env={})


def test_invalid_json_and_missing_file(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{nope")
    with pytest.raises(SettingsError, match="not valid JSON"):
        load_settings(bad, env={})
    with pytest.raises(SettingsError, match="not found"):
        load_settings(tmp_path / "missing.json", env={})
    arr = tmp_path / "arr.json"
    arr.write_text("[]")
    with pytest.raises(SettingsError, match="JSON object"):
        load_settings(arr, env={})


def test_public_dict_lists_every_setting_with_resolved_paths(tmp_path):
    s = Settings(work_dir=str(tmp_path), reviewer_root=str(tmp_path)).validate()
    d = s.public_dict()
    assert d["Environment"] == "development"
    assert d["Port"] == 12001
    assert d["WorkDir"] == str(tmp_path.resolve())
    assert d["ReviewerRoot"] == str(tmp_path.resolve())
    assert "AvailableModels" in d and "MaxConcurrentJobs" in d
