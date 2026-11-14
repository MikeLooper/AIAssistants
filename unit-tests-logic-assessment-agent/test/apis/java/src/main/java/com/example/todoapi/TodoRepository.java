package com.example.todoapi;

import java.util.List;
import java.util.Optional;

/** Storage for to-do items. */
public interface TodoRepository {

    TodoItem add(TodoItem item);

    Optional<TodoItem> findById(int id);

    List<TodoItem> all();

    boolean remove(int id);
}
