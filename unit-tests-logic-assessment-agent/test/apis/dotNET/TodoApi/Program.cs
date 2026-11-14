using TodoApi;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddSingleton<ITodoRepository, InMemoryTodoRepository>();
builder.Services.AddSingleton<TodoService>();

var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.MapGet("/todos", (TodoService service, bool includeCompleted = false, int? minPriority = null) =>
    Results.Ok(service.ListTodos(includeCompleted, minPriority)));

app.MapGet("/todos/{id:int}", (int id, ITodoRepository repository) =>
    repository.FindById(id) is { } item ? Results.Ok(item) : Results.NotFound());

app.MapPost("/todos", (CreateTodoRequest request, TodoService service) =>
{
    try
    {
        var item = service.CreateTodo(request.Title, request.Priority);
        return Results.Created($"/todos/{item.Id}", item);
    }
    catch (ValidationException ex)
    {
        return Results.BadRequest(new { error = ex.Message });
    }
});

app.MapPut("/todos/{id:int}/complete", (int id, TodoService service) =>
{
    try
    {
        return Results.Ok(service.CompleteTodo(id));
    }
    catch (NotFoundException)
    {
        return Results.NotFound();
    }
});

app.MapPut("/todos/{id:int}/title", (int id, RenameTodoRequest request, TodoService service) =>
{
    try
    {
        return Results.Ok(service.RenameTodo(id, request.Title));
    }
    catch (ValidationException ex)
    {
        return Results.BadRequest(new { error = ex.Message });
    }
    catch (NotFoundException)
    {
        return Results.NotFound();
    }
});

app.MapDelete("/todos/{id:int}", (int id, TodoService service) =>
{
    try
    {
        service.DeleteTodo(id);
        return Results.NoContent();
    }
    catch (NotFoundException)
    {
        return Results.NotFound();
    }
});

app.Run();
