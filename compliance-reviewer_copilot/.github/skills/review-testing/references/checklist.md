# Checklist — Testing

| id | Check | Default severity | Source |
|----|-------|-------------------|--------|
| TST-01 | Most tests are fast unit tests; integration/E2E tests are fewer, per the test pyramid | Warning | https://martinfowler.com/articles/practical-test-pyramid.html |
| TST-02 | A code coverage tool is configured and reported (in CI or locally) | Warning | https://martinfowler.com/articles/practical-test-pyramid.html |
| TST-03 | Tests assert real behavior/outputs, not just "did not throw" | Warning | https://martinfowler.com/articles/practical-test-pyramid.html |
| TST-04 | Mocking is used judiciously; tests don't mock so much that they no longer test real logic | Warning | https://martinfowler.com/articles/practical-test-pyramid.html |
| TST-05 | Tests are independent and don't rely on execution order or shared mutable state | Warning | https://martinfowler.com/articles/practical-test-pyramid.html |
| TST-06 | The test suite runs automatically in CI on every change | Error | https://martinfowler.com/articles/practical-test-pyramid.html |
