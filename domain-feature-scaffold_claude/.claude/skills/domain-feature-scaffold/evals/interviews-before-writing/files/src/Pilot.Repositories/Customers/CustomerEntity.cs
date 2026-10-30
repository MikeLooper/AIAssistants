namespace Pilot.Repositories.Customers;

/// <summary>Row of the Customers table.</summary>
public sealed class CustomerEntity
{
    /// <summary>Primary key.</summary>
    public int Id { get; set; }

    /// <summary>Company name.</summary>
    public string CompanyName { get; set; } = string.Empty;

    /// <summary>Contact person.</summary>
    public string? ContactName { get; set; }

    /// <summary>Country.</summary>
    public string? Country { get; set; }
}
