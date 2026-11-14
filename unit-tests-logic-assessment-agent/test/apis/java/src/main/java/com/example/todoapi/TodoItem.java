package com.example.todoapi;

/** A single to-do item. Priority runs from 1 (lowest) to 5 (highest). */
public class TodoItem {

    private int id;
    private String title;
    private int priority;
    private boolean completed;

    public TodoItem() {
    }

    public TodoItem(int id, String title, int priority) {
        this.id = id;
        this.title = title;
        this.priority = priority;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public int getPriority() {
        return priority;
    }

    public void setPriority(int priority) {
        this.priority = priority;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void setCompleted(boolean completed) {
        this.completed = completed;
    }
}
