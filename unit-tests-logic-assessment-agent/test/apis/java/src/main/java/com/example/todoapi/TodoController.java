package com.example.todoapi;

import java.net.URI;
import java.util.List;
import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.todoapi.TodoRequests.CreateTodoRequest;
import com.example.todoapi.TodoRequests.RenameTodoRequest;

/** HTTP endpoints for to-do items. */
@RestController
public class TodoController {

    private final TodoService service;
    private final TodoRepository repository;

    public TodoController(TodoService service, TodoRepository repository) {
        this.service = service;
        this.repository = repository;
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "ok");
    }

    @GetMapping("/todos")
    public List<TodoItem> list(@RequestParam(defaultValue = "false") boolean includeCompleted,
                               @RequestParam(required = false) Integer minPriority) {
        return service.listTodos(includeCompleted, minPriority);
    }

    @GetMapping("/todos/{id}")
    public ResponseEntity<TodoItem> getById(@PathVariable int id) {
        return repository.findById(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping("/todos")
    public ResponseEntity<TodoItem> create(@RequestBody CreateTodoRequest request) {
        TodoItem item = service.createTodo(request.title(), request.priority());
        return ResponseEntity.created(URI.create("/todos/" + item.getId())).body(item);
    }

    @PutMapping("/todos/{id}/complete")
    public TodoItem complete(@PathVariable int id) {
        return service.completeTodo(id);
    }

    @PutMapping("/todos/{id}/title")
    public TodoItem rename(@PathVariable int id, @RequestBody RenameTodoRequest request) {
        return service.renameTodo(id, request.title());
    }

    @DeleteMapping("/todos/{id}")
    public ResponseEntity<Void> delete(@PathVariable int id) {
        service.deleteTodo(id);
        return ResponseEntity.noContent().build();
    }

    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<Map<String, String>> handleValidation(ValidationException ex) {
        return ResponseEntity.badRequest().body(Map.of("error", ex.getMessage()));
    }

    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<Void> handleNotFound(NotFoundException ex) {
        return ResponseEntity.notFound().build();
    }
}
