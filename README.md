# chess-tactics-cli

A small, local-first Python CLI for drilling chess tactics from FEN
positions: find the best move, check your answer, and track your accuracy
and streak in a local JSON file. Includes a quiz mode to practice over and
over.

A fan project by **Dylan Asdale / Asdale Dynamics, LLC** (Indiana, formed
October 2026). No game assets are included or distributed. This is not
affiliated with or endorsed by any chess platform, publisher, or rights
holder.

Built for beginners: everything runs on your own computer, nothing is sent
anywhere, and there are no accounts or API keys.

## Install

You need Python 3.10 or newer. Get a copy of this project, then install it:

```bash
git clone <this-repo>
cd chess-tactics-cli
pip install -e .
```

The `python-chess` package is installed automatically and does the heavy
lifting of understanding FEN positions and chess moves.

## What a tactic is

A tactic is a single chess position (written in FEN notation) together with
the best move for that position. You add a tactic, then practice finding the
best move. The CLI remembers how many times you've tried, how many you got
right, your current streak, and your best streak.

## Usage

### Add a tactic

Give the CLI a FEN position and the best move for it:

```bash
chess-tactics-cli add \
  --fen "rnbqkbnr/pppppppp/8/8/4N3/8/PPPPPPPP/RNBQKB1R b KQkq - 1 3" \
  --best-move "e5" \
  --theme fork \
  --difficulty beginner
```

The FEN is validated before the tactic is saved, and the best move is
checked to make sure it's actually legal on that position. You can also add
`--theme` (for example: fork, pin, skewer) and `--difficulty`
(beginner, intermediate, advanced) to help organize your drills.

### List your tactics

```bash
chess-tactics-cli list
```

You'll see each tactic's ID, theme, difficulty, attempts, correct answers,
accuracy, and current streak.

### Show one tactic

```bash
chess-tactics-cli show <tactic-id>
```

This prints the tactic's details and an ASCII rendering of the board so you
can see the position without opening a separate chess board.

### Drill a single tactic

```bash
chess-tactics-cli solve <tactic-id>
```

The CLI shows you the board and asks for the best move. Type it in SAN
notation (like `e4` or `Nxe5`) or UCI notation (like `e2e4`). It tells you
whether you're right, shows the correct move if you're wrong, and updates
your accuracy and streak.

Example:

```text
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . N . . .
. . . . . . . .
P P P P P P P P
R N B Q K B . R
Turn: Black
Theme: fork  Difficulty: beginner
Best move: e5

Correct! e5 is the best move.
Accuracy: 100%  Streak: 1  Best streak: 1
```

### Quiz mode

```bash
chess-tactics-cli quiz
```

Quiz mode cycles through your tactics, showing unsolved ones first. For each
position it asks for the best move, then reports your session accuracy and
streak. Type `q` to quit at any time. When you finish, your results are
saved to your local JSON file.

### Stats and delete

```bash
chess-tactics-cli stats
chess-tactics-cli delete <tactic-id>
```

`stats` shows your totals across all tactics. `delete` removes a tactic you
no longer want to drill.

### Use a different storage file

By default everything is saved to `tactics.json` in the current folder. Use
`--storage` to pick another location:

```bash
chess-tactics-cli --storage ~/my-tactics.json add ...
```

## Storage

All your data lives in a local JSON file. Nothing is sent anywhere. No
accounts, no API keys, no network.

## Tests

```bash
pip install pytest
pytest
```

Tests cover FEN parsing/validation, scoring (accuracy and streaks), JSON
storage round-trips, and CLI behavior.

## Credits

Built by Dylan Asdale, registered nurse turned AI author and founder of
**Asdale Dynamics, LLC** — beginner-friendly AI education, books and guides,
and practical local-first tools. See *The Massive AI Manual* and
dylanasdale.github.io.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.
