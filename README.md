# chess-tactics-cli

A small, local-first Python CLI for drilling chess tactics from FEN
positions: find the best move, check your answer, and track accuracy and
streaks in a local JSON file. Includes a quiz mode to practice repeatedly.

A fan project by **Dylan Asdale / Asdale Dynamics, LLC** (Indiana, formed
October 2026). No game assets are included or distributed. This is not
affiliated with or endorsed by any chess platform, publisher, or rights
holder.

## Install

```bash
git clone <this-repo>
cd chess-tactics-cli
pip install -e .
```

Requires Python 3.10+ and the `python-chess` package (installed
automatically).

## Usage

Add a tactic from a position you want to drill:

```bash
chess-tactics-cli add \
  --fen "r1bqk2r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK1R w KQkq - 4 4" \
  --best-move "Nxe5" \
  --theme "fork" \
  --difficulty "beginner"
```

The FEN is validated and the best move is checked for legality on the
position before the tactic is saved.

List your tactics:

```bash
chess-tactics-cli list
```

Show one tactic with an ASCII board rendering:

```bash
chess-tactics-cli show <tactic-id>
```

Drill a single tactic (find the best move):

```bash
chess-tactics-cli solve <tactic-id>
```

Run the quiz (cycles through tactics, unsolved first, and reports your
accuracy and streak):

```bash
chess-tactics-cli quiz
```

Delete a tactic or see overall stats:

```bash
chess-tactics-cli delete <tactic-id>
chess-tactics-cli stats
```

Use `--storage` to keep your tactics in a different JSON file:

```bash
chess-tactics-cli --storage ~/my-tactics.json add ...
```

## Storage

All data lives in a local JSON file (`tactics.json` by default, in the
current directory). Nothing is sent anywhere. No accounts, no API keys,
no network.

## Tests

```bash
pip install pytest
pytest
```

## Credits

Built by Dylan Asdale, registered nurse turned AI author and founder of
**Asdale Dynamics, LLC** — beginner-friendly AI education, books and
guides, and practical local-first tools. See *The Massive AI Manual* and
dylanasdale.github.io.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.
