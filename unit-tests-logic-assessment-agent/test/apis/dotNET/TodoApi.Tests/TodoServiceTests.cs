using Moq;

namespace TodoApi.Tests;

public class TodoServiceTests
{
    private readonly InMemoryTodoRepository repository = new();
    private readonly TodoService service;

    public TodoServiceTests()
    {
        service = new TodoService(repository);
    }

    // ---- CreateTodo

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public void CreateTodo_BlankTitle_ThrowsValidationException(string? title)
    {
        var ex = Assert.Throws<ValidationException>(() => service.CreateTodo(title, 3));

        Assert.Equal("Title is required.", ex.Message);
    }

    [Fact]
    public void CreateTodo_PriorityZero_ThrowsValidationException()
    {
        var ex = Assert.Throws<ValidationException>(() => service.CreateTodo("Buy milk", 0));

        Assert.Equal("Priority must be between 1 and 5.", ex.Message);
    }

    [Fact]
    public void CreateTodo_ValidInput_StoresTrimmedItem()
    {
        var item = service.CreateTodo("  Buy milk  ", 2);

        Assert.Equal("Buy milk", item.Title);
        Assert.Equal(2, item.Priority);
        Assert.False(item.IsCompleted);
        Assert.Same(item, repository.FindById(item.Id));
    }

    // ---- CompleteTodo

    [Fact]
    public void CompleteTodo_OpenItem_MarksItCompleted()
    {
        var item = service.CreateTodo("Walk the dog", 3);

        var result = service.CompleteTodo(item.Id);

        Assert.True(result.IsCompleted);
        Assert.True(repository.FindById(item.Id)!.IsCompleted);
    }

    [Fact]
    public void CompleteTodo_AlreadyCompleted_ReturnsItem()
    {
        var item = service.CreateTodo("Pay rent", 5);
        service.CompleteTodo(item.Id);

        var result = service.CompleteTodo(item.Id);

        Assert.NotNull(result);
    }

    // ---- ListTodos

    [Fact]
    public void ListTodos_Default_ExcludesCompletedItemsAndSortsByPriority()
    {
        var low = service.CreateTodo("Low", 1);
        var high = service.CreateTodo("High", 5);
        var done = service.CreateTodo("Done", 4);
        service.CompleteTodo(done.Id);

        var result = service.ListTodos();

        Assert.Equal(new[] { high.Id, low.Id }, result.Select(i => i.Id));
    }

    [Fact]
    public void ListTodos_IncludeCompleted_ReturnsAllItemsSortedByPriority()
    {
        var low = service.CreateTodo("Low", 1);
        var done = service.CreateTodo("Done", 4);
        service.CompleteTodo(done.Id);

        var result = service.ListTodos(includeCompleted: true);

        Assert.Equal(new[] { done.Id, low.Id }, result.Select(i => i.Id));
    }

    // ---- DeleteTodo

    [Fact]
    public void DeleteTodo_ExistingItem_Deletes()
    {
        var item = service.CreateTodo("Old task", 2);

        service.DeleteTodo(item.Id);
    }

    [Fact]
    public void DeleteTodo_MissingItem_ThrowsNotFoundException()
    {
        var ex = Assert.Throws<NotFoundException>(() => service.DeleteTodo(404));

        Assert.Equal(404, ex.Id);
    }

    // ---- RenameTodo

    [Fact]
    public void RenameTodo_ValidTitle_UpdatesTitle()
    {
        var repo = new Mock<ITodoRepository>();
        repo.Setup(r => r.FindById(It.IsAny<int>())).Returns(new TodoItem { Id = 1, Title = "Old", Priority = 3 });
        var mockedService = new TodoService(repo.Object);

        var result = mockedService.RenameTodo(42, "  New title ");

        Assert.Equal("New title", result.Title);
    }

    [Fact]
    public void RenameTodo_BlankTitle_ThrowsValidationException()
    {
        var repo = new Mock<ITodoRepository>();
        var mockedService = new TodoService(repo.Object);

        Assert.Throws<ValidationException>(() => mockedService.RenameTodo(1, " "));
    }

    // ---- PriorityLabel

    [Theory]
    [InlineData(1, "low")]
    [InlineData(2, "low")]
    [InlineData(4, "high")]
    [InlineData(5, "high")]
    public void PriorityLabel_ReturnsLabel(int priority, string expected)
    {
        Assert.Equal(expected, TodoService.PriorityLabel(priority));
    }
}
