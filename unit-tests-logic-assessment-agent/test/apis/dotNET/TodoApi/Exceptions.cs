namespace TodoApi;

/// <summary>Thrown when a request value breaks a business rule.</summary>
public class ValidationException(string message) : Exception(message);

/// <summary>Thrown when no to-do has the requested id.</summary>
public class NotFoundException(int id) : Exception($"To-do {id} was not found.")
{
    public int Id { get; } = id;
}
