---
paths:
  - "test/Bruno/**"
---

# Bruno collection

- The collection root is `test/Bruno/PilotApiDotNet`. Collection-wide OAuth2 auth and headers are defined only in `test/Bruno/PilotApiDotNet/opencollection.yml`. The outer `test/Bruno/opencollection.yml` has no effect.
- Requests under `System` must carry no `auth` of their own, so they don't inherit the collection token. Setting `none` on the folder does not stop inheritance.
- The `.env` file next to `opencollection.yml` is created from `.env.example` and is git-ignored.
- If the collection is open in the Bruno app, saving from its UI overwrites hand edits to these files.
