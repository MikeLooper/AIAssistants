namespace TodoApi;

/// <summary>Thread-safe, in-memory to-do storage.</summary>
public class InMemoryTodoRepository : ITodoRepository
{
    private readonly Dictionary<int, TodoItem> items = new();
    private readonly Lock gate = new();
    private int nextId = 1;

    public TodoItem Add(TodoItem item)
    {
        lock (gate)
        {
            item.Id = nextId++;
            items[item.Id] = item;
            return item;
        }
    }

    public TodoItem? FindById(int id)
    {
        lock (gate)
        {
            return items.TryGetValue(id, out var item) ? item : null;
        }
    }

    public IReadOnlyList<TodoItem> All()
    {
        lock (gate)
        {
            return items.Values.OrderBy(i => i.Id).ToList();
        }
    }

    public bool Remove(int id)
    {
        lock (gate)
        {
            return items.Remove(id);
        }
    }
}
