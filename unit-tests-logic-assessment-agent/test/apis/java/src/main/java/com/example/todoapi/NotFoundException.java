package com.example.todoapi;

/** Thrown when no to-do has the requested id. */
public class NotFoundException extends RuntimeException {

    private final int id;

    public NotFoundException(int id) {
        super("To-do " + id + " was not found.");
        this.id = id;
    }

    public int getId() {
        return id;
    }
}
