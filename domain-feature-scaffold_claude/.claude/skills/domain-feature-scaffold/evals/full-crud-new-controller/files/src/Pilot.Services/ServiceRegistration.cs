using Microsoft.Extensions.DependencyInjection;
using Pilot.Services.Customers;

namespace Pilot.Services;

/// <summary>Registers the service layer for dependency injection.</summary>
public static class ServiceRegistration
{
    /// <summary>Adds every service.</summary>
    public static IServiceCollection AddPilotServices(this IServiceCollection services)
    {
        services.AddScoped<ICustomerService, CustomerService>();
        return services;
    }
}
