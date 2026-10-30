namespace Pilot.Repositories.Customers;

/// <summary>Data access for the Customers table.</summary>
public interface ICustomerRepository
{
    /// <summary>Gets one customer, or null when it does not exist.</summary>
    Task<CustomerEntity?> GetByIdAsync(int id, CancellationToken cancellationToken = default);

    /// <summary>Gets all customers.</summary>
    Task<IReadOnlyList<CustomerEntity>> GetAllAsync(CancellationToken cancellationToken = default);
}
