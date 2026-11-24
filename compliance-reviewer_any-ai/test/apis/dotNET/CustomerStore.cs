using System.Text.Json;

namespace TodoApi;

public static class CustomerStore
{
    public static List<Customer> Items = new();

    public static void Load(string contentRoot)
    {
        var path = Path.Combine(contentRoot, "Data", "customers.seed.json");
        var json = File.ReadAllText(path);
        Items = JsonSerializer.Deserialize<List<Customer>>(json, new JsonSerializerOptions(JsonSerializerDefaults.Web)) ?? new();
    }
}
