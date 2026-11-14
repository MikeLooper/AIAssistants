package com.example.todoapi;

import java.util.Comparator;
import java.util.List;
import java.util.stream.Stream;

import org.springframework.stereotype.Service;

/** Business rules for to-do items. */
@Service
public class TodoService {

    public static final int MAX_TITLE_LENGTH = 100;

    private final TodoRepository repository;

    public TodoService(TodoRepository repository) {
        this.repository = repository;
    }

    public TodoItem createTodo(String title, int priority) {
        if (title == null || title.isBlank()) {
            throw new ValidationException("Title is required.");
        }

        String trimmed = title.strip();
        if (trimmed.length() > MAX_TITLE_LENGTH) {
            throw new ValidationException("Title must be " + MAX_TITLE_LENGTH + " characters or fewer.");
        }

        if (priority < 1 || priority > 5) {
            throw new ValidationException("Priority must be between 1 and 5.");
        }

        return repository.add(new TodoItem(0, trimmed, priority));
    }

    public TodoItem completeTodo(int id) {
        TodoItem item = repository.findById(id).orElseThrow(() -> new NotFoundException(id));
        if (item.isCompleted()) {
            return item; // already completed: nothing to change
        }

        item.setCompleted(true);
        return item;
    }

    public List<TodoItem> listTodos(boolean includeCompleted, Integer minPriority) {
        Stream<TodoItem> items = repository.all().stream();
        if (!includeCompleted) {
            items = items.filter(i -> !i.isCompleted());
        }

        if (minPriority != null) {
            items = items.filter(i -> i.getPriority() >= minPriority);
        }

        return items
                .sorted(Comparator.comparingInt(TodoItem::getPriority).reversed().thenComparingInt(TodoItem::getId))
                .toList();
    }

    public void deleteTodo(int id) {
        if (!repository.remove(id)) {
            throw new NotFoundException(id);
        }
    }

    public TodoItem renameTodo(int id, String newTitle) {
        if (newTitle == null || newTitle.isBlank()) {
            throw new ValidationException("Title is required.");
        }

        TodoItem item = repository.findById(id).orElseThrow(() -> new NotFoundException(id));
        item.setTitle(newTitle.strip());
        return item;
    }

    public static String priorityLabel(int priority) {
        return switch (priority) {
            case 1, 2 -> "low";
            case 3 -> "medium";
            case 4, 5 -> "high";
            default -> "unknown";
        };
    }
}
