"""Start comp-review-api: python run.py [--config PATH] [--host HOST] [--port PORT] [--reload]

Settings come from appsettings.json (or --config / COMP_REVIEW_API_CONFIG) and COMP_REVIEW_API_* variables;
--host and --port override them for this run."""

from __future__ import annotations

import argparse
import logging
import os
import sys

import uvicorn

from comp_review_api.config import CONFIG_PATH_ENV, SettingsError, load_settings


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Start comp-review-api (Swagger UI at /swagger).")
    p.add_argument("--config", help="Settings file (default: appsettings.json next to this script).")
    p.add_argument("--host", help="Interface to bind (default: the Host setting).")
    p.add_argument("--port", type=int, help="Port to bind (default: the Port setting, 12001).")
    p.add_argument("--reload", action="store_true", help="Restart when the code changes (development).")
    args = p.parse_args(argv)
    if args.config:
        os.environ[CONFIG_PATH_ENV] = args.config  # also read by the factory in a --reload worker
    try:
        settings = load_settings()
    except SettingsError as e:
        print(f"configuration error: {e}", file=sys.stderr)
        return 2
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    uvicorn.run("comp_review_api.main:create_app", factory=True, host=args.host or settings.host,
                port=args.port or settings.port, reload=args.reload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
