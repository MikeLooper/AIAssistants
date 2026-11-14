namespace TodoApi;

/// <summary>Storage for to-do items.</summary>
public interface ITodoRepository
{
    TodoItem Add(TodoItem item);

    TodoItem? FindById(int id);

    IReadOnlyList<TodoItem> All();

    bool Remove(int id);
}
