package com.example.todoapi;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;

import org.springframework.stereotype.Repository;

/** Thread-safe, in-memory to-do storage. */
@Repository
public class InMemoryTodoRepository implements TodoRepository {

    private final Map<Integer, TodoItem> items = new TreeMap<>();
    private int nextId = 1;

    @Override
    public synchronized TodoItem add(TodoItem item) {
        item.setId(nextId++);
        items.put(item.getId(), item);
        return item;
    }

    @Override
    public synchronized Optional<TodoItem> findById(int id) {
        return Optional.ofNullable(items.get(id));
    }

    @Override
    public synchronized List<TodoItem> all() {
        return new ArrayList<>(items.values());
    }

    @Override
    public synchronized boolean remove(int id) {
        return items.remove(id) != null;
    }
}
