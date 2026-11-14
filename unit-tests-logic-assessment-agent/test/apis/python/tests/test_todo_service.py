import unittest
from unittest.mock import Mock

from errors import NotFoundError, ValidationError
from models import TodoItem
from todo_repository import InMemoryTodoRepository, TodoRepository
from todo_service import TodoService, priority_label


class TodoServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryTodoRepository()
        self.service = TodoService(self.repository)

    # ---- create_todo

    def test_create_todo_blank_title_raises_validation_error(self):
        for title in (None, "", "   "):
            with self.subTest(title=title):
                with self.assertRaises(ValidationError) as ctx:
                    self.service.create_todo(title, 3)
                self.assertEqual("Title is required.", str(ctx.exception))

    def test_create_todo_priority_zero_raises_validation_error(self):
        with self.assertRaises(ValidationError) as ctx:
            self.service.create_todo("Buy milk", 0)

        self.assertEqual("Priority must be between 1 and 5.", str(ctx.exception))

    def test_create_todo_valid_input_stores_trimmed_item(self):
        item = self.service.create_todo("  Buy milk  ", 2)

        self.assertEqual("Buy milk", item.title)
        self.assertEqual(2, item.priority)
        self.assertFalse(item.completed)
        self.assertIs(item, self.repository.find_by_id(item.id))

    # ---- complete_todo

    def test_complete_todo_open_item_marks_it_completed(self):
        item = self.service.create_todo("Walk the dog", 3)

        result = self.service.complete_todo(item.id)

        self.assertTrue(result.completed)
        self.assertTrue(self.repository.find_by_id(item.id).completed)

    def test_complete_todo_already_completed_returns_item(self):
        item = self.service.create_todo("Pay rent", 5)
        self.service.complete_todo(item.id)

        result = self.service.complete_todo(item.id)

        self.assertIsNotNone(result)

    # ---- list_todos

    def test_list_todos_default_excludes_completed_items_and_sorts_by_priority(self):
        low = self.service.create_todo("Low", 1)
        high = self.service.create_todo("High", 5)
        done = self.service.create_todo("Done", 4)
        self.service.complete_todo(done.id)

        result = self.service.list_todos()

        self.assertEqual([high.id, low.id], [i.id for i in result])

    def test_list_todos_include_completed_returns_all_items_sorted_by_priority(self):
        low = self.service.create_todo("Low", 1)
        done = self.service.create_todo("Done", 4)
        self.service.complete_todo(done.id)

        result = self.service.list_todos(include_completed=True)

        self.assertEqual([done.id, low.id], [i.id for i in result])

    # ---- delete_todo

    def test_delete_todo_existing_item_deletes(self):
        item = self.service.create_todo("Old task", 2)

        self.service.delete_todo(item.id)

    def test_delete_todo_missing_item_raises_not_found_error(self):
        with self.assertRaises(NotFoundError) as ctx:
            self.service.delete_todo(404)

        self.assertEqual(404, ctx.exception.todo_id)

    # ---- rename_todo

    def test_rename_todo_valid_title_updates_title(self):
        repo = Mock(spec=TodoRepository)
        repo.find_by_id.return_value = TodoItem(id=1, title="Old", priority=3)
        mocked_service = TodoService(repo)

        result = mocked_service.rename_todo(42, "  New title ")

        self.assertEqual("New title", result.title)

    def test_rename_todo_blank_title_raises_validation_error(self):
        mocked_service = TodoService(Mock(spec=TodoRepository))

        with self.assertRaises(ValidationError):
            mocked_service.rename_todo(1, " ")

    # ---- priority_label

    def test_priority_label_returns_label(self):
        for priority, expected in ((1, "low"), (2, "low"), (4, "high"), (5, "high")):
            with self.subTest(priority=priority):
                self.assertEqual(expected, priority_label(priority))


if __name__ == "__main__":
    unittest.main()
