"""Validate the Compliance Reviewer against the C# MCP server test app (test/mcps/dotNET, stdio transport).

Usage: python test/logic/test_mcp_dotnet.py [--tool claude|copilot] [--min-found 90] [--help]
"""

import sys

from harness import main

if __name__ == "__main__":
    sys.exit(main("mcps", "dotNET"))
