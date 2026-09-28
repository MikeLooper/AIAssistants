# Skill: ut-logic-assess-test-to-element-mapping

## Goal
Compute element-level and logic-level test coverage sets under strict evidence rules.

## Inputs
- `Class Elements`
- `Class Logic`
- `Unit Test Classes`
- `Unit Test Elements`

## Outputs
### Untested Classes
- Code classes in `Classes` with no related `Unit Test Classes` records.

### Tested Class Elements
Each record must contain:
- `Code class name`
- `Unit test class name`
- `Name of method or property`
- `Type of element` (`Method` or `Property`)

### Not Tested Class Elements
Each record must contain:
- `Code class name`
- `Unit test class name`
- `Name of method or property`
- `Type of element` (`Method` or `Property`)

### Logic Covered
Each record must contain:
- `Code class name`
- `Unit test class name`
- `Name of method or property`
- `Type of element` (`Method` or `Property`)
- `Logic branch summary`

### Logic Not Covered
Each record must contain:
- `Code class name`
- `Unit test class name`
- `Name of method or property`
- `Type of element` (`Method` or `Property`)
- `Logic branch summary`

## Strict Evidence Policy
Count as covered only when both are true:
1. The test interacts with the target element explicitly.
2. The test asserts a behavior outcome tied to the targeted branch or element.

Do not count:
- Naming conventions alone.
- Comments indicating intent without assertions.
- Unresolved helper indirection.

## Algorithm
1. Build class-to-tests mapping from `Unit Test Classes`.
2. For each class with tests, mark element as tested if explicit test evidence exists.
3. Set difference per class yields `Not Tested Class Elements`.
4. For each logic branch in `Class Logic`, mark covered only if one or more mapped tests assert that branch behavior.
5. Set difference per class yields `Logic Not Covered`.
