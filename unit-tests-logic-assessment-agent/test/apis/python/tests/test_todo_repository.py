import unittest

from models import TodoItem
from todo_repository import InMemoryTodoRepository


class InMemoryTodoRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryTodoRepository()

    def test_add_assigns_sequential_ids(self):
        first = self.repository.add(TodoItem(id=0, title="First", priority=1))
        second = self.repository.add(TodoItem(id=0, title="Second", priority=2))

        self.assertEqual(1, first.id)
        self.assertEqual(2, second.id)

    def test_find_by_id_existing_item_returns_it(self):
        added = self.repository.add(TodoItem(id=0, title="Find me", priority=3))

        self.assertIs(added, self.repository.find_by_id(added.id))

    def test_find_by_id_missing_item_returns_none(self):
        self.assertIsNone(self.repository.find_by_id(99))

    def test_all_returns_items_ordered_by_id(self):
        self.repository.add(TodoItem(id=0, title="A", priority=1))
        self.repository.add(TodoItem(id=0, title="B", priority=5))

        self.assertEqual(["A", "B"], [i.title for i in self.repository.all()])

    def test_remove_existing_item_returns_true_and_removes_it(self):
        added = self.repository.add(TodoItem(id=0, title="Remove me", priority=2))

        self.assertTrue(self.repository.remove(added.id))
        self.assertIsNone(self.repository.find_by_id(added.id))

    def test_remove_missing_item_returns_false(self):
        self.assertFalse(self.repository.remove(42))


if __name__ == "__main__":
    unittest.main()
