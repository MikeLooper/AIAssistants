"""Validate the Compliance Reviewer against the C# UI test app (test/uis/dotNET).

Usage: python test/logic/test_ui_dotnet.py [--tool claude|copilot] [--min-found 90] [--help]
"""

import sys

from harness import main

if __name__ == "__main__":
    sys.exit(main("uis", "dotNET"))
