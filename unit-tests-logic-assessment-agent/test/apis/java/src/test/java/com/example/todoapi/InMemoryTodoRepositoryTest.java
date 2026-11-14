package com.example.todoapi;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;

import org.junit.jupiter.api.Test;

class InMemoryTodoRepositoryTest {

    private final InMemoryTodoRepository repository = new InMemoryTodoRepository();

    @Test
    void add_assignsSequentialIds() {
        TodoItem first = repository.add(new TodoItem(0, "First", 1));
        TodoItem second = repository.add(new TodoItem(0, "Second", 2));

        assertEquals(1, first.getId());
        assertEquals(2, second.getId());
    }

    @Test
    void findById_existingItem_returnsIt() {
        TodoItem added = repository.add(new TodoItem(0, "Find me", 3));

        assertSame(added, repository.findById(added.getId()).orElseThrow());
    }

    @Test
    void findById_missingItem_returnsEmpty() {
        assertTrue(repository.findById(99).isEmpty());
    }

    @Test
    void all_returnsItemsOrderedById() {
        repository.add(new TodoItem(0, "A", 1));
        repository.add(new TodoItem(0, "B", 5));

        assertEquals(List.of("A", "B"), repository.all().stream().map(TodoItem::getTitle).toList());
    }

    @Test
    void remove_existingItem_returnsTrueAndRemovesIt() {
        TodoItem added = repository.add(new TodoItem(0, "Remove me", 2));

        assertTrue(repository.remove(added.getId()));
        assertTrue(repository.findById(added.getId()).isEmpty());
    }

    @Test
    void remove_missingItem_returnsFalse() {
        assertFalse(repository.remove(42));
    }
}
