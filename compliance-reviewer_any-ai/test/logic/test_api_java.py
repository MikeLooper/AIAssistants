"""Validate the Compliance Reviewer against the Java API test app (test/apis/java).

Usage: python test/logic/test_api_java.py [--tool claude|copilot] [--min-found 90] [--help]
"""

import sys

from harness import main

if __name__ == "__main__":
    sys.exit(main("apis", "java"))
