using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Pilot.Repositories.Customers;

namespace Pilot.Repositories;

/// <summary>Registers the repository layer for dependency injection.</summary>
public static class RepositoryRegistration
{
    /// <summary>Adds the DbContext and every repository.</summary>
    public static IServiceCollection AddPilotRepositories(this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<PilotDbContext>(o => o.UseSqlServer(configuration.GetConnectionString("Pilot")));
        services.AddScoped<ICustomerRepository, CustomerRepository>();
        return services;
    }
}
