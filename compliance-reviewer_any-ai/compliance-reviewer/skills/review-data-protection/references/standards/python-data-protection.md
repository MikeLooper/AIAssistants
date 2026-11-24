# Django REST framework serializer fields — localized summary

- Sources: www.django-rest-framework.org — API Guide "Serializers" @ encode/django-rest-framework
  9421957437b9fecd0ddb9f4806e2872fad525a7b (`docs/api-guide/serializers.md`, 2026-11-10)
- Localized: 2026-11-24 · Elements: www.django-rest-framework.org 2 (prefix `PYD-`; counted in this skill's per-website budget)
- Applies when language `python` is detected and `djangorestframework` is a dependency. FastAPI `response_model` and
  Pydantic models aren't localized: judge them with the BOP elements.
- Level: `SHOULD` for "strongly recommended" and other recommendations; **(Default)** marks an element that states
  framework behaviour. Levels are informational: every Finding takes its check's default severity.
- Citation: `Finding.url` = citation base + `#` + primary (first) anchor. `Finding.standard` = `"<source name> — <element ID>"`.

| Key | Citation base | Pinned commit | Source name for `Finding.standard` |
|-----|---------------|---------------|------------------------------------|
| drf | https://www.django-rest-framework.org/api-guide/serializers/ | 94219574 (2026-11-10) | Django REST framework — Serializers |

| ID | Level | Requirement (summary) | Code/config evidence | Check | Anchor(s) |
|----|-------|-----------------------|----------------------|-------|-----------|
| PYD-01 | SHOULD | `ModelSerializer` lists every serialized field explicitly in `Meta.fields`; `fields = '__all__'` (and `exclude`) make new model fields appear in responses automatically. | `fields = '__all__'` on a serializer for a model with personal data | DPR-02 | drf#specifying-which-fields-to-include |
| PYD-02 | SHOULD | **(Default)** Input-only fields such as passwords are made `write_only` through `extra_kwargs`; `extra_kwargs` and `read_only_fields` are ignored for fields declared explicitly on the serializer (set the option on the field itself). | password or secret-answer field readable in responses; option set in `extra_kwargs` for an explicitly declared field | DPR-02 | drf#additional-keyword-arguments, drf#specifying-read-only-fields |
