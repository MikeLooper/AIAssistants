using Pilot.Domain.Customers;

namespace Pilot.Services.Customers;

/// <summary>Customer operations used by the API.</summary>
public interface ICustomerService
{
    /// <summary>Gets one customer, or null when it does not exist.</summary>
    Task<CustomerDto?> GetByIdAsync(int id, CancellationToken cancellationToken = default);

    /// <summary>Gets all customers.</summary>
    Task<IReadOnlyList<CustomerDto>> GetAllAsync(CancellationToken cancellationToken = default);
}
