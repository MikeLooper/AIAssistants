"""Validate the Compliance Reviewer against the Python MCP server test app (test/mcps/python, stdio transport).

Usage: python test/logic/test_mcp_python.py [--tool claude|copilot] [--min-found 90] [--help]
"""

import sys

from harness import main

if __name__ == "__main__":
    sys.exit(main("mcps", "python"))
