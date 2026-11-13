"""Validate the Compliance Reviewer against the Java MCP server test app (test/mcps/java, stdio transport).

Usage: python test/logic/test_mcp_java.py [--tool claude|copilot] [--min-found 90] [--help]
"""

import sys

from harness import main

if __name__ == "__main__":
    sys.exit(main("mcps", "java"))
