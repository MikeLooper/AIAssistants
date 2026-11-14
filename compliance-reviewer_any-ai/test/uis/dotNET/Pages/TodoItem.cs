namespace TodoUi.Pages;

public class TodoItem
{
    public int Id { get; set; }

    public string Title { get; set; } = "";

    public int Priority { get; set; }

    public bool IsComplete { get; set; }
}
