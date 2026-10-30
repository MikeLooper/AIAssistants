using Microsoft.EntityFrameworkCore;
using Pilot.Repositories.Customers;

namespace Pilot.Repositories;

/// <summary>EF Core context for the Pilot database.</summary>
public sealed class PilotDbContext(DbContextOptions<PilotDbContext> options) : DbContext(options)
{
    /// <summary>Rows of the Customers table.</summary>
    public DbSet<CustomerEntity> Customers => Set<CustomerEntity>();

    /// <inheritdoc />
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<CustomerEntity>(e =>
        {
            e.ToTable("Customers");
            e.HasKey(x => x.Id);
            e.Property(x => x.Id).HasColumnName("CustomerID");
            e.Property(x => x.CompanyName).HasMaxLength(40).IsRequired();
            e.Property(x => x.ContactName).HasMaxLength(30);
            e.Property(x => x.Country).HasMaxLength(15);
        });
    }
}
