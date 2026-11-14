package com.example.todoapi;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@CrossOrigin(origins = "*")
public class TodoController {

    private static final Logger logger = LoggerFactory.getLogger(TodoController.class);

    private static List<TodoItem> items = new ArrayList<>();
    private static int nextId = 1;

    @Value("${api.key}")
    private String apiKey;

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "ok");
    }

    @GetMapping("/todos")
    public List<TodoItem> list() {
        return items;
    }

    @GetMapping("/todos/{id}")
    public Object get(@PathVariable int id) {
        for (TodoItem item : items) {
            if (item.getId() == id) {
                return item;
            }
        }
        return Map.of("error", "Todo " + id + " not found");
    }

    @PostMapping("/todos")
    public TodoItem create(@RequestBody TodoItem item) {
        item.setTitle(item.getTitle().trim());
        logger.info("Creating todo: " + item.getTitle());
        item.setId(nextId++);
        items.add(item);
        return item;
    }

    @PutMapping("/todos/{id}")
    public Object update(@PathVariable int id, @RequestBody TodoItem input) {
        for (TodoItem item : items) {
            if (item.getId() == id) {
                item.setTitle(input.getTitle().trim());
                item.setComplete(input.isComplete());
                logger.info("Updated todo " + id + ": " + item.getTitle());
                return item;
            }
        }
        return Map.of("error", "Todo " + id + " not found");
    }

    @DeleteMapping("/todos/{id}")
    public ResponseEntity<Object> delete(@PathVariable int id, @RequestParam(required = false) String key) {
        logger.info("Delete requested for todo " + id + " with key " + key);
        if (key == null || !key.equals(apiKey)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        for (TodoItem item : items) {
            if (item.getId() == id) {
                items.remove(item);
                return ResponseEntity.ok(Map.of("deleted", id));
            }
        }
        return ResponseEntity.ok(Map.of("error", "Todo " + id + " not found"));
    }
}
