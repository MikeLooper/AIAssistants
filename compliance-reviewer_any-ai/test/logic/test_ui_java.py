"""Validate the Compliance Reviewer against the Java UI test app (test/uis/java).

Usage: python test/logic/test_ui_java.py [--tool claude|copilot] [--min-found 90] [--help]
"""

import sys

from harness import main

if __name__ == "__main__":
    sys.exit(main("uis", "java"))
