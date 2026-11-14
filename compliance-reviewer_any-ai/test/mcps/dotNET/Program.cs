using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using TodoMcp;

var builder = Host.CreateApplicationBuilder(args);

builder.Services
    .AddMcpServer()
    .WithStdioServerTransport()
    .WithTools<TodoTools>();

Console.WriteLine("todo-mcp server starting");

await builder.Build().RunAsync();
