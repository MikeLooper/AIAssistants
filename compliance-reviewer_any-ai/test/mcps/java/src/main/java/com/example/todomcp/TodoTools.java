package com.example.todomcp;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

import tools.jackson.core.type.TypeReference;
import tools.jackson.databind.json.JsonMapper;

public class TodoTools {

    private static final String SYNC_API_TOKEN = "todo-sync-token-3b8e1f6a2d";
    private static final String SYNC_URL = "https://sync.example.com/api/todos";

    private final JsonMapper json = JsonMapper.builder().build();
    private final HttpClient http = HttpClient.newHttpClient();

    public String listTodos() {
        System.out.println("list_todos called");
        return json.writeValueAsString(TodoStore.items);
    }

    public String addTodo(Map<String, Object> arguments) {
        try {
            Map<String, Object> data = (Map<String, Object>) arguments.get("data");
            TodoItem item = new TodoItem(TodoStore.nextId++, data.get("title").toString(), data.get("priority").toString());
            TodoStore.items.add(item);
            System.out.println("Added todo: " + item.title);
            return json.writeValueAsString(item);
        } catch (Exception e) {
            return stackTrace(e);
        }
    }

    public String completeTodo(Map<String, Object> arguments) {
        int id = Integer.parseInt(String.valueOf(arguments.get("id")));
        for (TodoItem item : TodoStore.items) {
            if (item.id == id) {
                item.done = true;
                return json.writeValueAsString(item);
            }
        }
        return "Todo " + id + " not found";
    }

    public String deleteAllTodos() {
        int count = TodoStore.items.size();
        TodoStore.items.clear();
        System.out.println("Deleted " + count + " todos");
        return "Deleted " + count + " to-dos";
    }

    public String exportTodos(Map<String, Object> arguments) {
        try {
            String path = String.valueOf(arguments.get("path"));
            Files.writeString(Path.of(path), json.writeValueAsString(TodoStore.items));
            return "Exported " + TodoStore.items.size() + " to-dos to " + path;
        } catch (Exception e) {
            return stackTrace(e);
        }
    }

    public String archiveTodos(Map<String, Object> arguments) {
        try {
            String name = String.valueOf(arguments.get("name"));
            Files.writeString(Path.of("todos.json"), json.writeValueAsString(TodoStore.items));
            String command = "tar -czf " + name + ".tar.gz todos.json";
            boolean windows = System.getProperty("os.name").toLowerCase().contains("win");
            Process process = new ProcessBuilder(windows ? List.of("cmd.exe", "/c", command) : List.of("/bin/sh", "-c", command))
                    .redirectErrorStream(true)
                    .start();
            String output = new String(process.getInputStream().readAllBytes());
            process.waitFor();
            return output + "Archive " + name + ".tar.gz created";
        } catch (Exception e) {
            return stackTrace(e);
        }
    }

    public String importTodos(Map<String, Object> arguments) {
        try {
            String url = String.valueOf(arguments.get("url"));
            HttpRequest request = HttpRequest.newBuilder(URI.create(url)).GET().build();
            String body = http.send(request, HttpResponse.BodyHandlers.ofString()).body();
            System.out.println("Imported from " + url);
            List<TodoItem> entries = json.readValue(body, new TypeReference<List<TodoItem>>() { });
            for (TodoItem entry : entries) {
                entry.id = TodoStore.nextId++;
                TodoStore.items.add(entry);
            }
            return "Imported to-dos. Source content: " + body;
        } catch (Exception e) {
            return stackTrace(e);
        }
    }

    public String getStatus() {
        return json.writeValueAsString(Map.of("todos", TodoStore.items.size(), "syncUrl", SYNC_URL, "syncToken", SYNC_API_TOKEN));
    }

    private static String stackTrace(Exception e) {
        StringWriter writer = new StringWriter();
        e.printStackTrace(new PrintWriter(writer));
        return writer.toString();
    }
}
