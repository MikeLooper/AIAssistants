"""Storage for to-do items."""

import threading
from typing import Protocol

from models import TodoItem


class TodoRepository(Protocol):
    """Storage contract used by the service."""

    def add(self, item: TodoItem) -> TodoItem: ...

    def find_by_id(self, todo_id: int) -> TodoItem | None: ...

    def all(self) -> list[TodoItem]: ...

    def remove(self, todo_id: int) -> bool: ...


class InMemoryTodoRepository:
    """Thread-safe, in-memory to-do storage."""

    def __init__(self) -> None:
        self._items: dict[int, TodoItem] = {}
        self._next_id = 1
        self._lock = threading.Lock()

    def add(self, item: TodoItem) -> TodoItem:
        with self._lock:
            item.id = self._next_id
            self._next_id += 1
            self._items[item.id] = item
            return item

    def find_by_id(self, todo_id: int) -> TodoItem | None:
        with self._lock:
            return self._items.get(todo_id)

    def all(self) -> list[TodoItem]:
        with self._lock:
            return sorted(self._items.values(), key=lambda i: i.id)

    def remove(self, todo_id: int) -> bool:
        with self._lock:
            return self._items.pop(todo_id, None) is not None
