"""Validate the Compliance Reviewer against the Python UI test app (test/uis/python).

Usage: python test/logic/test_ui_python.py [--tool claude|copilot] [--min-found 90] [--help]
"""

import sys

from harness import main

if __name__ == "__main__":
    sys.exit(main("uis", "python"))
