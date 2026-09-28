# Checklist — Software Lifecycle

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| SL-01 | CI runs build and automated tests on every push/PR | Error | https://slsa.dev/spec/v1.0/requirements |
| SL-02 | A documented release process exists (tagging, changelog, publish step) | Warning | https://semver.org/ |
| SL-03 | Version numbers follow SemVer (MAJOR.MINOR.PATCH with meaningful bumps) | Warning | https://semver.org/#semantic-versioning-specification-semver |
| SL-04 | Branching model is documented and enforced (e.g. protected main, required reviews) | Warning | https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development |
| SL-05 | Build provenance/signing or a reproducible build process is in place | Information | https://slsa.dev/spec/v1.0/requirements |
| SL-06 | Dependency updates are automated or regularly scheduled | Warning | https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development |
| SL-07 | A `SECURITY.md` or equivalent vulnerability-reporting process exists | Information | https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/nist-sp-800-218-secure-software-development |
| SL-08 | A changelog or release notes are kept up to date | Information | https://semver.org/ |
