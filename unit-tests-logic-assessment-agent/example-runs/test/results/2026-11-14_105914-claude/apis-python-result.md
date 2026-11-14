# apis-python — PASS

- Tool: claude (--tool)
- Run ID: `20261114-105915` — report: C:\Working\Storage\Dev\GitHub\AIAssistants\unit-tests-logic-assessment-agent\docs\coverage-review-20261114-105915.md
- Duration: 381 s, cost $1.10
- Fresh build and unit-test run: succeeded (C:\Users\Michael\AppData\Local\Python\pythoncore-3.14-64\python.exe -m compileall -q .; C:\Users\Michael\AppData\Local\Python\pythoncore-3.14-64\python.exe -m unittest discover -s tests, 1 s)
- Reviewer metrics: totalPaths 47, totalProblems 27, problemPct 57.45, severity 11 / 9 / 3 / 4
- Gaps found: 10/10 (100%; need 9 for 90%)
- Control paths classified Uncovered (false positives): 0

## Seeded gaps

| Gap | Category | Result | Classified as | Matching row |
|---|---|---|---|---|
| G1 CreateTodo: title longer than 100 characters is never tested | Boundary | found | covered, uncovered | P-03 \| Trimmed title length `> MAX_TITLE_LENGTH` (100) \| — \| — \| Uncovered \| No test constructs a title longer than 100 characters. |
| G2 CreateTodo: only the priority < 1 half of 'priority < 1 \|\| priority > 5' is tested | Compound decision | found | covered, uncovered | P-05 \| `priority > 5` \| — \| — \| Uncovered \| No test uses a priority above 5. |
| G3 CompleteTodo: the 'id not found' error branch is never tested | Error branch | found | uncovered | P-01 \| `repository.find_by_id` returns `None` \| — \| — \| Uncovered \| No test calls `complete_todo` with a non-existent id; the `NotFoundError` branch is never exercised. |
| G4 CompleteTodo: the 'already completed' test only asserts the result is not null (weak assertion) | Weak assertion | found | partial | P-02 \| Item found, already `completed` \| `test_complete_todo_already_completed_returns_item` \| Weak — only `assertIsNotNone(result)`; does not assert `result.completed` remains `True`, nor identity/idempotency \| Parti... |
| G5 ListTodos: the minPriority filter is never tested | Decision branch | found | uncovered | P-03 \| `min_priority is not None` \| — \| — \| Uncovered \| Neither test passes the `min_priority` argument; the filter branch never executes. |
| G6 DeleteTodo: the successful delete is executed by a test with no assertion | Absent assertion | found | uncovered | P-02 \| `repository.remove` returns `True` \| `test_delete_todo_existing_item_deletes` \| **Absent** — the test body calls `self.service.delete_todo(item.id)` with no `assert*` statement at all ("execution without verifi... |
| G7 PriorityLabel: the 'medium' (priority 3) arm is never tested | Decision branch | found | uncovered | P-02 \| `priority_label` \| `3` \| **Uncovered** \| — \| — \| [todo_service.py#L70-L71](../test/apis/python/todo_service.py) \| — |
| G8 PriorityLabel: the default 'unknown' arm (out-of-range priority) is never tested | Boundary | found | uncovered | P-04 \| `priority` is any other value (default `case _`) \| — \| — \| Uncovered \| No test uses an out-of-range value (e.g., `0`, `6`, `-1`) to exercise the `"unknown"` fall-through. |
| G9 RenameTodo: the 'id not found' branch is hidden by a mock that returns an item for any id (mock bypass) | Mock bypass | found | uncovered | P-01 \| `rename_todo` \| `new_title is None` \| **Uncovered** \| — \| — \| [todo_service.py#L55-L56](../test/apis/python/todo_service.py) \| — |
| G10 API layer (endpoints and their error mapping) has no unit tests | Unmapped unit | found | uncovered | P-01 \| Called (straight-line) \| — \| — \| Uncovered \| No test suite exercises `main.py` at all. |

## Control paths (should be Covered)

| Control | Result | Classified as | Matching row |
|---|---|---|---|
| C1 CreateTodo: blank title (null, empty, whitespace) throws a validation error | confirmed Covered | covered | P-01 \| `title is None` \| `test_create_todo_blank_title_raises_validation_error` (subTest `title=None`) \| Strong — exact message asserted (`assertEqual("Title is required.", str(ctx.exception))`) \| Covered \| — |
| C2 CreateTodo: valid input stores and returns the trimmed item | confirmed Covered | covered | P-06 \| `create_todo` \| valid input (happy path) \| Covered \| `test_create_todo_valid_input_stores_trimmed_item` \| Strong \| [todo_service.py#L27](../test/apis/python/todo_service.py) \| [test_todo_service.py#L30-L36](../... |
| C3 CompleteTodo: an open item is marked completed | confirmed Covered | covered | P-03 \| Item found, not yet completed \| `test_complete_todo_open_item_marks_it_completed` \| Strong — `assertTrue` on both the returned item and the repository-persisted item \| Covered \| — |
| C4 ListTodos: completed items are hidden unless includeCompleted is true | confirmed Covered | covered | P-01 \| `include_completed` is `False` \| `test_list_todos_default_excludes_completed_items_and_sorts_by_priority` \| Strong — exact remaining id list/order asserted \| Covered \| — |
| C5 DeleteTodo: a missing id throws a not-found error | confirmed Covered | covered, partial | P-01 \| Constructor called with any `todo_id` \| `test_delete_todo_missing_item_raises_not_found_error` \| Partial — `todo_id` attribute is strongly asserted (`assertEqual(404, ctx.exception.todo_id)`), but the formatted... |
| C6 PriorityLabel: priority 4 and 5 return 'high' | **missed** (no matching row) | — | — |
| C7 Repository FindById: a missing id returns null / empty / None | confirmed Covered | covered, partial | P-01 \| Constructor called (straight-line) \| Exercised implicitly via `setUp` in every test; initial state indirectly implied by `test_add_assigns_sequential_ids` (first id is `1`, implying `_next_id` started at `1`) a... |

## Other problems reported (not scored): 7

| Section | Classification | Row |
|---|---|---|
| Method: `InMemoryTodoRepository.all` | uncovered | P-01 \| `_items` is empty \| — \| — \| Uncovered \| No test calls `all()` on an empty repository. |
| Method: `TodoService.list_todos` | uncovered | P-05 \| `repository.all()` returns an empty list \| — \| — \| Uncovered \| No test calls `list_todos` on an empty repository. |
| Method: `TodoService.rename_todo` | uncovered | P-01 \| `new_title is None` \| — \| — \| Uncovered \| `test_rename_todo_blank_title_raises_validation_error` only exercises `new_title=" "`; no test passes `None` to `rename_todo`. |
| Method: `TodoService.rename_todo` | uncovered | P-03 \| Title valid, `repository.find_by_id` returns `None` \| — \| — \| Uncovered \| No test combines a non-blank title with an id the mocked/real repository doesn't have. |
| Function: `priority_label` | uncovered | P-02 \| `priority` is `3` \| — \| — \| Uncovered \| The subTest loop `((1,"low"),(2,"low"),(4,"high"),(5,"high"))` skips `3`; the `"medium"` case is never exercised. |
| Run Tallies | partial | Partially Covered \| 3 |
| Run Tallies | uncovered | Uncovered \| 24 |
