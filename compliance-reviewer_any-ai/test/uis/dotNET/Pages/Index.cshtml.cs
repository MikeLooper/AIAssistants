using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace TodoUi.Pages;

[IgnoreAntiforgeryToken]
public class IndexModel : PageModel
{
    public static List<TodoItem> Items = new();
    private static int nextId = 1;

    private readonly IConfiguration configuration;

    public IndexModel(IConfiguration configuration)
    {
        this.configuration = configuration;
    }

    public void OnGet()
    {
    }

    public IActionResult OnPostAdd(string title, string priority, string? returnUrl)
    {
        var item = new TodoItem { Id = nextId++, Title = title };
        try
        {
            item.Priority = int.Parse(priority);
        }
        catch
        {
        }
        Items.Add(item);
        System.IO.File.AppendAllText("todo-ui.log", DateTime.Now + " Added todo: " + title + Environment.NewLine);
        return Redirect(returnUrl ?? "/");
    }

    public IActionResult OnPostComplete(int id)
    {
        var item = Items.FirstOrDefault(t => t.Id == id);
        if (item != null)
        {
            item.IsComplete = true;
        }
        // var removed = Items.RemoveAll(t => t.IsComplete);
        // System.IO.File.AppendAllText("todo-ui.log", "Removed " + removed + Environment.NewLine);
        return RedirectToPage();
    }

    public IActionResult OnGetClear(string password)
    {
        if (password == configuration["AdminPassword"])
        {
            Items.Clear();
            System.IO.File.AppendAllText("todo-ui.log", DateTime.Now + " Cleared all todos" + Environment.NewLine);
        }
        return RedirectToPage();
    }
}
