"""Allow running the CLI as ``python -m chess_tactics``."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
