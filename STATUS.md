# STATUS

chess-tactics-cli — local-first Python CLI for drilling chess tactics from
FEN positions.
Commit: initial commit, branch: master.

## What was built

A small Python CLI (`chess_tactics` package) that lets you drill chess
tactics from FEN positions: you supply a FEN and the best move, the CLI
validates both with python-chess, then you can solve tactics one at a time
or run a quiz. Accuracy and streaks are tracked per tactic and overall in a
local JSON file.

Modules:
- `models.py` — `Tactic` dataclass (id, fen, best_move, theme, difficulty,
  created_at, attempts, correct, streak, best_streak, last_attempted,
  solved_at) with `accuracy`/`solved` properties, `to_dict`/`from_dict`
  serialization, and a `Tactic.new` factory.
- `fen.py` — `validate_fen`, `board_from_fen`, and `board_ascii` (ASCII
  board rendering with side to move) backed by python-chess.
- `scoring.py` — `ScoreTracker`: records attempts, computes accuracy,
  current streak, and best streak.
- `storage.py` — `Storage`: atomic read/write of tactics to a local JSON
  file (temp file + os.replace), with add/load/find/delete/update.
- `quiz.py` — `check_move` (SAN or UCI input, canonical SAN comparison
  against the best move) and `pick_quiz_tactic` (unsolved first, then
  least-attempted).
- `cli.py` — argparse commands: `add`, `list`, `show`, `solve`, `quiz`,
  `stats`, `delete`; `--storage` option (default `tactics.json`).
- `__main__.py` — supports `python -m chess_tactics`.
- Console script entry point: `chess-tactics-cli`.

Tests (`tests/`): `test_fen.py` (valid/invalid FEN, turn and move number,
ASCII rendering), `test_scoring.py` (accuracy, streak reset, best streak
tracking), `test_storage.py` (add/load/delete/update roundtrip, atomic
write with no `.tmp` leftovers, corrupt/non-list JSON handling), `test_cli`
(add validation, list, stats, show/delete of missing id, quiz empty,
solve correct/incorrect feedback).

Also included: `LICENSE` (MIT, "Copyright (c) 2026 Asdale Dynamics, LLC"),
`README.md` (credits Asdale Dynamics, LLC), `pyproject.toml`, `.gitignore`.
Fan project, no game assets, no network, no secrets, no personal data.

## How to run

```bash
pip install -e .        # requires python-chess (installed automatically)
chess-tactics-cli --help

chess-tactics-cli add \
  --fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" \
  --best-move e4 \
  --theme opening --difficulty beginner

chess-tactics-cli list
chess-tactics-cli show <tactic-id>
chess-tactics-cli solve <tactic-id>
chess-tactics-cli quiz
chess-tactics-cli stats
chess-tactics-cli delete <tactic-id>

# Or without installing:
python3 -m chess_tactics --storage tactics.json ...
```

All data stays in a local JSON file (`tactics.json` by default). Nothing is
sent anywhere.

## Verification results

- `pip install -e . --break-system-packages`: OK (console script
  `chess-tactics-cli` installed at ~/.local/bin/chess-tactics-cli)
- `python3 -m pytest -q`: 21 passed
- `python3 -m ruff check chess_tactics tests`: All checks passed
- `python3 -m ruff format --check chess_tactics tests`: All files formatted
- Manual CLI flows verified: add (invalid FEN rejected with exit 1; invalid
  move rejected), list, show (ASCII board + turn), solve (correct feedback
  with accuracy/streak, incorrect feedback resetting streak), quiz
  (quit flow + summary), stats, delete (missing id exit 1),
  `python3 -m chess_tactics` entry point.

Python 3.13.5; dependency: python-chess 1.11.2 (imported as `chess`).

## Known gaps

- The best move must be supplied by the user; there is no chess engine, so
  moves are not verified against engine analysis.
- Move answers are accepted in SAN or UCI and compared as canonical SAN;
  equivalent-looking notations are normalized by python-chess.
- Quiz picks unsolved/least-attempted tactics with randomness; no
  spaced-repetition scheduling.
- No edit command (delete and re-add instead).
- Storage path defaults to `tactics.json` in the current directory; use
  `--storage` for another location.
- No `.github/workflows` files (per project constraints), no CI configured.
