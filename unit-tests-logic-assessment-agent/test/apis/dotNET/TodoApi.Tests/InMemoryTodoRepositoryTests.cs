namespace TodoApi.Tests;

public class InMemoryTodoRepositoryTests
{
    private readonly InMemoryTodoRepository repository = new();

    [Fact]
    public void Add_AssignsSequentialIds()
    {
        var first = repository.Add(new TodoItem { Title = "First", Priority = 1 });
        var second = repository.Add(new TodoItem { Title = "Second", Priority = 2 });

        Assert.Equal(1, first.Id);
        Assert.Equal(2, second.Id);
    }

    [Fact]
    public void FindById_ExistingItem_ReturnsIt()
    {
        var added = repository.Add(new TodoItem { Title = "Find me", Priority = 3 });

        var found = repository.FindById(added.Id);

        Assert.Same(added, found);
    }

    [Fact]
    public void FindById_MissingItem_ReturnsNull()
    {
        Assert.Null(repository.FindById(99));
    }

    [Fact]
    public void All_ReturnsItemsOrderedById()
    {
        repository.Add(new TodoItem { Title = "A", Priority = 1 });
        repository.Add(new TodoItem { Title = "B", Priority = 5 });

        var all = repository.All();

        Assert.Equal(new[] { "A", "B" }, all.Select(i => i.Title));
    }

    [Fact]
    public void Remove_ExistingItem_ReturnsTrueAndRemovesIt()
    {
        var added = repository.Add(new TodoItem { Title = "Remove me", Priority = 2 });

        Assert.True(repository.Remove(added.Id));
        Assert.Null(repository.FindById(added.Id));
    }

    [Fact]
    public void Remove_MissingItem_ReturnsFalse()
    {
        Assert.False(repository.Remove(42));
    }
}
