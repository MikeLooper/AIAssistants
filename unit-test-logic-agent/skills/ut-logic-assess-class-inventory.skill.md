# Skill: ut-logic-assess-class-inventory

## Goal
Identify production code classes and their elements.

## Inputs
- Source files in supported languages: C#, Java, Python.

## Outputs
### Classes
- List of code class names.

### Class Elements
Each record must contain:
- `Code class name`
- `Name of method or property`
- `Type of element` (`Method` or `Property`)

## Rules
- Exclude test files and generated files where detectable.
- For Python, include `@property` and setter/deleter as `Property` unless split mode is explicitly enabled.
- For Java, treat bean-style property accessors as `Method` by default unless a property abstraction is requested.
- Normalize element identity as `ClassName::ElementName::ElementType`.

## Quality Checks
- No duplicate `Class Elements` records by normalized identity.
- Every `Class Elements` record must reference a class present in `Classes`.
