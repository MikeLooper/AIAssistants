"""Business rules for to-do items."""

from errors import NotFoundError, ValidationError
from models import TodoItem
from todo_repository import TodoRepository

MAX_TITLE_LENGTH = 100


class TodoService:
    """Creates, completes, lists, renames and deletes to-do items."""

    def __init__(self, repository: TodoRepository) -> None:
        self._repository = repository

    def create_todo(self, title: str | None, priority: int) -> TodoItem:
        if title is None or not title.strip():
            raise ValidationError("Title is required.")

        trimmed = title.strip()
        if len(trimmed) > MAX_TITLE_LENGTH:
            raise ValidationError(f"Title must be {MAX_TITLE_LENGTH} characters or fewer.")

        if priority < 1 or priority > 5:
            raise ValidationError("Priority must be between 1 and 5.")

        return self._repository.add(TodoItem(id=0, title=trimmed, priority=priority))

    def complete_todo(self, todo_id: int) -> TodoItem:
        item = self._repository.find_by_id(todo_id)
        if item is None:
            raise NotFoundError(todo_id)

        if item.completed:
            return item  # already completed: nothing to change

        item.completed = True
        return item

    def list_todos(self, include_completed: bool = False, min_priority: int | None = None) -> list[TodoItem]:
        items = self._repository.all()
        if not include_completed:
            items = [i for i in items if not i.completed]

        if min_priority is not None:
            items = [i for i in items if i.priority >= min_priority]

        return sorted(items, key=lambda i: (-i.priority, i.id))

    def delete_todo(self, todo_id: int) -> None:
        if not self._repository.remove(todo_id):
            raise NotFoundError(todo_id)

    def rename_todo(self, todo_id: int, new_title: str | None) -> TodoItem:
        if new_title is None or not new_title.strip():
            raise ValidationError("Title is required.")

        item = self._repository.find_by_id(todo_id)
        if item is None:
            raise NotFoundError(todo_id)

        item.title = new_title.strip()
        return item


def priority_label(priority: int) -> str:
    match priority:
        case 1 | 2:
            return "low"
        case 3:
            return "medium"
        case 4 | 5:
            return "high"
        case _:
            return "unknown"
