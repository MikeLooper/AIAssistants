"""Business errors raised by the to-do service."""


class ValidationError(Exception):
    """A request value breaks a business rule."""


class NotFoundError(Exception):
    """No to-do has the requested id."""

    def __init__(self, todo_id: int) -> None:
        super().__init__(f"To-do {todo_id} was not found.")
        self.todo_id = todo_id
