using Pilot.Domain.Customers;
using Pilot.Repositories.Customers;

namespace Pilot.Services.Customers;

/// <summary>Default implementation of <see cref="ICustomerService"/>.</summary>
public sealed class CustomerService(ICustomerRepository customerRepository) : ICustomerService
{
    /// <inheritdoc />
    public async Task<CustomerDto?> GetByIdAsync(int id, CancellationToken cancellationToken = default)
    {
        var entity = await customerRepository.GetByIdAsync(id, cancellationToken);
        return entity is null ? null : new CustomerDto(entity.Id, entity.CompanyName, entity.ContactName, entity.Country);
    }

    /// <inheritdoc />
    public async Task<IReadOnlyList<CustomerDto>> GetAllAsync(CancellationToken cancellationToken = default)
    {
        var entities = await customerRepository.GetAllAsync(cancellationToken);
        return entities.Select(e => new CustomerDto(e.Id, e.CompanyName, e.ContactName, e.Country)).ToList();
    }
}
