using Pilot.Repositories;
using Pilot.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddPilotRepositories(builder.Configuration);
builder.Services.AddPilotServices();

var app = builder.Build();

app.MapControllers();

app.Run();
