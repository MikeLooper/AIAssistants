package com.example.todoapi;

/** Request bodies accepted by {@link TodoController}. */
public final class TodoRequests {

    private TodoRequests() {
    }

    /** Body of POST /todos. */
    public record CreateTodoRequest(String title, int priority) {
    }

    /** Body of PUT /todos/{id}/title. */
    public record RenameTodoRequest(String title) {
    }
}
