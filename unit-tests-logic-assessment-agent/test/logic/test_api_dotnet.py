"""Validate the Unit Test Coverage Reviewer against the C# API test app (test/apis/dotNET).

Usage: python test/logic/test_api_dotnet.py [--tool claude|copilot] [--min-found 90] [--help]
"""

import sys

from harness import main

if __name__ == "__main__":
    sys.exit(main("dotNET"))
