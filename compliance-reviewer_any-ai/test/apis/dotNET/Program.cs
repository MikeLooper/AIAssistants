using TodoApi;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddCors(options =>
    options.AddDefaultPolicy(policy => policy.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod()));

var app = builder.Build();

app.Use(async (context, next) =>
{
    try
    {
        await next();
    }
    catch (Exception ex)
    {
        context.Response.StatusCode = 500;
        await context.Response.WriteAsync(ex.ToString());
    }
});

app.UseSwagger();
app.UseSwaggerUI();
app.UseCors();

var apiKey = app.Configuration["ApiKey"];
var logger = app.Logger;

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.MapGet("/todos", () => TodoStore.Items);

app.MapGet("/todos/{id:int}", (int id) =>
{
    var item = TodoStore.Items.FirstOrDefault(t => t.Id == id);
    if (item == null)
    {
        return Results.Ok(new { error = "Todo " + id + " not found" });
    }
    return Results.Ok(item);
});

app.MapPost("/todos", (TodoItem item) =>
{
    item.Title = item.Title!.Trim();
    logger.LogInformation("Creating todo: " + item.Title);
    item.Id = TodoStore.NextId++;
    TodoStore.Items.Add(item);
    return Results.Ok(item);
});

app.MapPut("/todos/{id:int}", (int id, TodoItem input) =>
{
    var item = TodoStore.Items.FirstOrDefault(t => t.Id == id);
    if (item == null)
    {
        return Results.Ok(new { error = "Todo " + id + " not found" });
    }
    item.Title = input.Title!.Trim();
    item.IsComplete = input.IsComplete;
    logger.LogInformation("Updated todo " + id + ": " + item.Title);
    return Results.Ok(item);
});

app.MapDelete("/todos/{id:int}", (int id, string? key) =>
{
    logger.LogInformation("Delete requested for todo " + id + " with key " + key);
    if (key != apiKey)
    {
        return Results.Unauthorized();
    }
    var item = TodoStore.Items.FirstOrDefault(t => t.Id == id);
    if (item == null)
    {
        return Results.Ok(new { error = "Todo " + id + " not found" });
    }
    TodoStore.Items.Remove(item);
    return Results.Ok(new { deleted = id });
});

app.Run();
