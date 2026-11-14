namespace TodoApi;

/// <summary>Business rules for to-do items.</summary>
public class TodoService(ITodoRepository repository)
{
    public const int MaxTitleLength = 100;

    public TodoItem CreateTodo(string? title, int priority)
    {
        if (string.IsNullOrWhiteSpace(title))
        {
            throw new ValidationException("Title is required.");
        }

        var trimmed = title.Trim();
        if (trimmed.Length > MaxTitleLength)
        {
            throw new ValidationException($"Title must be {MaxTitleLength} characters or fewer.");
        }

        if (priority < 1 || priority > 5)
        {
            throw new ValidationException("Priority must be between 1 and 5.");
        }

        return repository.Add(new TodoItem { Title = trimmed, Priority = priority });
    }

    public TodoItem CompleteTodo(int id)
    {
        var item = repository.FindById(id) ?? throw new NotFoundException(id);
        if (item.IsCompleted)
        {
            return item; // already completed: nothing to change
        }

        item.IsCompleted = true;
        return item;
    }

    public IReadOnlyList<TodoItem> ListTodos(bool includeCompleted = false, int? minPriority = null)
    {
        IEnumerable<TodoItem> items = repository.All();
        if (!includeCompleted)
        {
            items = items.Where(i => !i.IsCompleted);
        }

        if (minPriority is int min)
        {
            items = items.Where(i => i.Priority >= min);
        }

        return items.OrderByDescending(i => i.Priority).ThenBy(i => i.Id).ToList();
    }

    public void DeleteTodo(int id)
    {
        if (!repository.Remove(id))
        {
            throw new NotFoundException(id);
        }
    }

    public TodoItem RenameTodo(int id, string? newTitle)
    {
        if (string.IsNullOrWhiteSpace(newTitle))
        {
            throw new ValidationException("Title is required.");
        }

        var item = repository.FindById(id) ?? throw new NotFoundException(id);
        item.Title = newTitle.Trim();
        return item;
    }

    public static string PriorityLabel(int priority) => priority switch
    {
        1 or 2 => "low",
        3 => "medium",
        4 or 5 => "high",
        _ => "unknown",
    };
}
