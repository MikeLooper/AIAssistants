package com.example.todomcp;

public class TodoItem {

    public int id;
    public String title;
    public String priority;
    public boolean done;

    public TodoItem() {
    }

    public TodoItem(int id, String title, String priority) {
        this.id = id;
        this.title = title;
        this.priority = priority;
    }
}
