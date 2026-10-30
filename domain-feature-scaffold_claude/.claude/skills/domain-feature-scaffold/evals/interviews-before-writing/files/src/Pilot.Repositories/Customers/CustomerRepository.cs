using Microsoft.EntityFrameworkCore;

namespace Pilot.Repositories.Customers;

/// <summary>EF Core implementation of <see cref="ICustomerRepository"/>.</summary>
public sealed class CustomerRepository(PilotDbContext dbContext) : ICustomerRepository
{
    /// <inheritdoc />
    public Task<CustomerEntity?> GetByIdAsync(int id, CancellationToken cancellationToken = default) =>
        dbContext.Customers.AsNoTracking().FirstOrDefaultAsync(c => c.Id == id, cancellationToken);

    /// <inheritdoc />
    public async Task<IReadOnlyList<CustomerEntity>> GetAllAsync(CancellationToken cancellationToken = default) =>
        await dbContext.Customers.AsNoTracking().OrderBy(c => c.Id).ToListAsync(cancellationToken);
}
