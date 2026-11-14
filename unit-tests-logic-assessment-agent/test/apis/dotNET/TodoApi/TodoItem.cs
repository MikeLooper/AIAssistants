namespace TodoApi;

/// <summary>A single to-do item.</summary>
public class TodoItem
{
    public int Id { get; set; }

    public string Title { get; set; } = string.Empty;

    /// <summary>1 (lowest) to 5 (highest).</summary>
    public int Priority { get; set; }

    public bool IsCompleted { get; set; }
}

/// <summary>Request body for POST /todos.</summary>
public record CreateTodoRequest(string? Title, int Priority);

/// <summary>Request body for PUT /todos/{id}/title.</summary>
public record RenameTodoRequest(string? Title);
