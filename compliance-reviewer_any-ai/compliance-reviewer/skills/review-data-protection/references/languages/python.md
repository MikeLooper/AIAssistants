# Detection signals — Python (Data Protection)

Detection signals only. They cite no standard. Report findings against the element IDs listed (defined in
`../standards/`). Django model-field, SQLAlchemy and Pydantic defaults aren't localized: judge explicit code only, and
add a `localized-standard-gap` note when a decision depends on a default.

| Signal (API, setting or pattern) | Look in | Indicates | Element(s) |
|---|---|---|---|
| `ssn = models.CharField(...)`, `card_number = Column(String)`, `iban: str` on ORM models with no encrypted field type or tokenization | models | Sensitive personal data stored in plaintext | A04-04, CSD-01 |
| `AES.new(key, AES.MODE_ECB)`, `hashlib.md5(email…)` as "protection", `Fernet` key stored in the same table | crypto helpers | Weak storage encryption or keys beside data | CSD-03, CSD-04 |
| `return jsonify(user.__dict__)`, `return user` from a FastAPI route without `response_model`, `model_dump()` of an ORM-backed model | routes, views | Over-exposure on output | BOP-03, BOP-01 |
| DRF `ModelSerializer` with `fields = '__all__'` or `exclude`; password fields without `write_only` | `serializers.py` | Over-exposure on output | PYD-01, PYD-02 |
| `request.args.get("email")`, `Query(email)`, `redirect(url_for(..., email=…))` | routes | Personal data in URLs | QSE-01 |
| `sentry_sdk.init(...)` without `data_collection` limits; `set_user({"email": …})` | entry point, settings | Error tracker sends user data | TPS-03 |
| `fixtures/*.json`, `conftest.py` factories, `seed*.py` with names, emails, card numbers, national IDs | tests, fixtures, seed scripts | Seed data (synthetic or real-looking) | SP122-06, RSV-01 |
