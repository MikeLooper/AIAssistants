"""Validate the Compliance Reviewer against the Python API test app (test/apis/python).

Usage: python test/logic/test_api_python.py [--tool claude|copilot] [--min-found 90] [--help]
"""

import sys

from harness import main

if __name__ == "__main__":
    sys.exit(main("apis", "python"))
