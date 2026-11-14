# Python signals — MCP Server

Lookup table for the official Python SDK (PyPI `mcp`; 2.x `from mcp.server import MCPServer`, 1.x
`from mcp.server.fastmcp import FastMCP`; low-level `mcp.server.lowlevel.Server`) and the standalone `fastmcp`
package. Signals, not elements: cite the elements in `../standards/`.

| Topic | Signals |
|---|---|
| Detection | `mcp` or `fastmcp` in `requirements*.txt`/`pyproject.toml`; `MCPServer(...)`, `FastMCP(...)`, `Server(...)` from `mcp.server.lowlevel`; `@mcp.tool()`, `@mcp.resource(...)`, `@mcp.prompt()` |
| Transport | stdio: `mcp.run()` (default), `mcp.run("stdio")`, `mcp.run(transport="stdio")`, `stdio_server()`; HTTP: `run("streamable-http")`, `run("sse")`, `streamable_http_app()`, `sse_app()` mounted in an ASGI app (then MCP-15 applies) |
| `stdout` writes (MCP-01) | `print(...)` without `file=sys.stderr`; `sys.stdout.write`; `logging.basicConfig(stream=sys.stdout)` or `logging.StreamHandler(sys.stdout)`; `rich`/`click.echo` to `stdout`. `logging.basicConfig()` with no stream writes to `stderr` (passes) |
| Tool definitions (MCP-04, MCP-05) | Name from `@mcp.tool(name=...)` or the function name; description from `description=` or the docstring; server instructions from `MCPServer(instructions=...)`. The input schema is generated from type hints: `dict`, `Any`, `object` or untyped parameters give an untyped schema; Pydantic models and `Annotated[str, Field(max_length=...)]` give a typed, bounded one |
| Validation (MCP-06) | Pydantic validates hinted types and `Field` constraints before the call; a `dict`/`Any` argument used with `.get(...)` and no checks fails |
| Annotations (MCP-10) | `@mcp.tool(annotations=ToolAnnotations(readOnlyHint=..., destructiveHint=..., idempotentHint=..., openWorldHint=...))` (`from mcp.types import ToolAnnotations`, or `mcp_types` in 2.x); confirmation via `ctx.elicit(...)` or a required `confirm: bool` parameter |
| Errors (MCP-07) | Raising `ToolError` (or any exception) yields an `isError` result; returning `traceback.format_exc()`, `repr(e)` or `str(e)` of an unexpected exception as normal output leaks internals and isn't flagged as an error |
| Credentials (MCP-11) | `os.environ[...]`/`os.getenv(...)` pass; module-level string constants holding tokens or keys fail |
| Limits (MCP-13) | `urllib.request.urlopen(url)` or `requests.get(url)`/`httpx.get(url)` without `timeout=`; `subprocess.run(...)` without `timeout=`; unbounded `.read()` of responses or files; no rate limiter around tool calls |
| Audit (MCP-14) | `logging` (to `stderr`) in tools, recording tool name, outcome and duration; `ctx.info(...)` sends log notifications to the client but isn't a server-side audit log |
