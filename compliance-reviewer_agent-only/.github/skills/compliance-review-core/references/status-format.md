# Status Reporting Format

## Todo List

The orchestrator's todo list has exactly one item per pipeline step (init, inventory, optional analyzers, one per chosen subject skill, aggregate, report). Batches within a subject are not separate todo items.

## Status Line

After each step completes, post exactly one status line (in addition to updating the todo list):

```
Step N/T: <name> done. Next: <name>. Remaining: <list>
Findings so far — Error: <n>, Warning: <n>, Information: <n>
```

- `N/T` is the step's position out of the total chosen steps (e.g. `Step 4/9`).
- `<name>` values are the human-readable step names (e.g. `Security — Identity & Access`), not file names.
- `Remaining` lists the human-readable names of steps not yet started, comma-separated. Use `none` when this is the last step.
- The findings totals are a running count across all steps completed so far in the run, taken from each step's `checkResults`/`findings`.
- On the final step (report), replace `Next` with `done` and state the report path instead of remaining steps.
