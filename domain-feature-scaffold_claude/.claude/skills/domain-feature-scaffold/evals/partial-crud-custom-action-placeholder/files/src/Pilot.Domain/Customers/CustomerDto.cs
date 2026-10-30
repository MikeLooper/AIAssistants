namespace Pilot.Domain.Customers;

/// <summary>Customer data exchanged between the API and the service layer.</summary>
public sealed record CustomerDto(int Id, string CompanyName, string? ContactName, string? Country);
