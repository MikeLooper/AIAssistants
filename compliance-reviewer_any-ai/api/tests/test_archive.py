import io
import stat
import zipfile

import pytest

from comp_review_api.archive import (ArchiveError, UploadTooLarge, extract_zip, review_root, safe_folder_name,
                                     save_upload)

from .conftest import make_zip

MB = 1024 * 1024


def _zip_file(tmp_path, files):
    p = tmp_path / "in.zip"
    p.write_bytes(make_zip(files))
    return p


def test_single_top_level_folder_becomes_the_target(tmp_path):
    z = _zip_file(tmp_path, {"myapp/src/main.py": "print(1)", "myapp/README.md": "hi", "__MACOSX/._x": "junk"})
    target = extract_zip(z, tmp_path / "out", MB, 100)
    assert target == tmp_path / "out" / "myapp"
    assert (target / "src" / "main.py").read_text() == "print(1)"


def test_loose_files_keep_the_extraction_folder_as_target(tmp_path):
    z = _zip_file(tmp_path, {"main.py": "x", "lib/util.py": "y"})
    assert extract_zip(z, tmp_path / "out", MB, 100) == tmp_path / "out"


def test_directory_entries_and_backslashes(tmp_path):
    z = _zip_file(tmp_path, {"app/": "", "app\\sub\\a.txt": "a"})
    target = extract_zip(z, tmp_path / "out", MB, 100)
    assert (target / "sub" / "a.txt").exists()


@pytest.mark.parametrize("name", ["../evil.txt", "a/../../evil.txt", "/etc/passwd", "C:/Windows/evil.txt"])
def test_unsafe_paths_are_rejected(tmp_path, name):
    z = _zip_file(tmp_path, {name: "x"})
    with pytest.raises(ArchiveError):
        extract_zip(z, tmp_path / "out", MB, 100)
    assert not (tmp_path / "evil.txt").exists()


def test_symlinks_are_rejected(tmp_path):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        info = zipfile.ZipInfo("link")
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        zf.writestr(info, "/etc/passwd")
    p = tmp_path / "l.zip"
    p.write_bytes(buf.getvalue())
    with pytest.raises(ArchiveError, match="symbolic link"):
        extract_zip(p, tmp_path / "out", MB, 100)


def test_limits(tmp_path):
    z = _zip_file(tmp_path, {f"f{i}.txt": "x" for i in range(5)})
    with pytest.raises(ArchiveError, match="5 files"):
        extract_zip(z, tmp_path / "a", MB, 4)
    big = _zip_file(tmp_path, {"big.bin": b"0" * 2048})
    with pytest.raises(ArchiveError, match="limit"):
        extract_zip(big, tmp_path / "b", 1024, 100)


def test_not_a_zip_and_empty_zip(tmp_path):
    p = tmp_path / "x.zip"
    p.write_text("not a zip")
    with pytest.raises(ArchiveError, match="not a zip"):
        extract_zip(p, tmp_path / "out", MB, 100)
    empty = _zip_file(tmp_path, {"dir/": ""})
    with pytest.raises(ArchiveError, match="no files"):
        extract_zip(empty, tmp_path / "out2", MB, 100)


def test_save_upload(tmp_path):
    dest = tmp_path / "sub" / "u.zip"
    assert save_upload(io.BytesIO(b"abc"), dest, 10) == 3
    assert dest.read_bytes() == b"abc"
    with pytest.raises(UploadTooLarge):
        save_upload(io.BytesIO(b"x" * 20), tmp_path / "big.zip", 10)


@pytest.mark.parametrize("filename, expected", [
    ("my app.zip", "my-app"), ("C:\\fake\\Proj.ZIP", "Proj"), ("../../x.zip", "x"), (None, "source"),
    ("???.zip", "source"), ("a" * 100 + ".zip", "a" * 64),
])
def test_safe_folder_name(filename, expected):
    assert safe_folder_name(filename) == expected


def test_review_root_with_one_file(tmp_path):
    (tmp_path / "only.txt").write_text("x")
    assert review_root(tmp_path) == tmp_path
