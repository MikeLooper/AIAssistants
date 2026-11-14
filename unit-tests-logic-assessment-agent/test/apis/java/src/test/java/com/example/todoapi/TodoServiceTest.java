package com.example.todoapi;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.NullSource;
import org.junit.jupiter.params.provider.ValueSource;

class TodoServiceTest {

    private final InMemoryTodoRepository repository = new InMemoryTodoRepository();
    private final TodoService service = new TodoService(repository);

    // ---- createTodo

    @ParameterizedTest
    @NullSource
    @ValueSource(strings = {"", "   "})
    void createTodo_blankTitle_throwsValidationException(String title) {
        ValidationException ex = assertThrows(ValidationException.class, () -> service.createTodo(title, 3));

        assertEquals("Title is required.", ex.getMessage());
    }

    @Test
    void createTodo_priorityZero_throwsValidationException() {
        ValidationException ex = assertThrows(ValidationException.class, () -> service.createTodo("Buy milk", 0));

        assertEquals("Priority must be between 1 and 5.", ex.getMessage());
    }

    @Test
    void createTodo_validInput_storesTrimmedItem() {
        TodoItem item = service.createTodo("  Buy milk  ", 2);

        assertEquals("Buy milk", item.getTitle());
        assertEquals(2, item.getPriority());
        assertFalse(item.isCompleted());
        assertSame(item, repository.findById(item.getId()).orElseThrow());
    }

    // ---- completeTodo

    @Test
    void completeTodo_openItem_marksItCompleted() {
        TodoItem item = service.createTodo("Walk the dog", 3);

        TodoItem result = service.completeTodo(item.getId());

        assertTrue(result.isCompleted());
        assertTrue(repository.findById(item.getId()).orElseThrow().isCompleted());
    }

    @Test
    void completeTodo_alreadyCompleted_returnsItem() {
        TodoItem item = service.createTodo("Pay rent", 5);
        service.completeTodo(item.getId());

        TodoItem result = service.completeTodo(item.getId());

        assertNotNull(result);
    }

    // ---- listTodos

    @Test
    void listTodos_default_excludesCompletedItemsAndSortsByPriority() {
        TodoItem low = service.createTodo("Low", 1);
        TodoItem high = service.createTodo("High", 5);
        TodoItem done = service.createTodo("Done", 4);
        service.completeTodo(done.getId());

        List<TodoItem> result = service.listTodos(false, null);

        assertEquals(List.of(high.getId(), low.getId()), result.stream().map(TodoItem::getId).toList());
    }

    @Test
    void listTodos_includeCompleted_returnsAllItemsSortedByPriority() {
        TodoItem low = service.createTodo("Low", 1);
        TodoItem done = service.createTodo("Done", 4);
        service.completeTodo(done.getId());

        List<TodoItem> result = service.listTodos(true, null);

        assertEquals(List.of(done.getId(), low.getId()), result.stream().map(TodoItem::getId).toList());
    }

    // ---- deleteTodo

    @Test
    void deleteTodo_existingItem_deletes() {
        TodoItem item = service.createTodo("Old task", 2);

        service.deleteTodo(item.getId());
    }

    @Test
    void deleteTodo_missingItem_throwsNotFoundException() {
        NotFoundException ex = assertThrows(NotFoundException.class, () -> service.deleteTodo(404));

        assertEquals(404, ex.getId());
    }

    // ---- renameTodo

    @Test
    void renameTodo_validTitle_updatesTitle() {
        TodoRepository repo = mock(TodoRepository.class);
        when(repo.findById(anyInt())).thenReturn(Optional.of(new TodoItem(1, "Old", 3)));
        TodoService mockedService = new TodoService(repo);

        TodoItem result = mockedService.renameTodo(42, "  New title ");

        assertEquals("New title", result.getTitle());
    }

    @Test
    void renameTodo_blankTitle_throwsValidationException() {
        TodoService mockedService = new TodoService(mock(TodoRepository.class));

        assertThrows(ValidationException.class, () -> mockedService.renameTodo(1, " "));
    }

    // ---- priorityLabel

    @ParameterizedTest
    @CsvSource({"1, low", "2, low", "4, high", "5, high"})
    void priorityLabel_returnsLabel(int priority, String expected) {
        assertEquals(expected, TodoService.priorityLabel(priority));
    }
}
