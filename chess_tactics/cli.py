"""Command-line interface for the chess tactics drill."""

from __future__ import annotations

import argparse
import random
import sys
from datetime import datetime, timezone

from .fen import board_ascii, validate_fen
from .models import Tactic
from .quiz import check_move
from .scoring import ScoreTracker
from .storage import Storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chess-tactics-cli",
        description="Drill chess tactics from FEN positions: find the best "
        "move, track accuracy and streaks in local JSON.",
    )
    parser.add_argument(
        "--storage",
        default="tactics.json",
        help="Path to the local JSON storage file (default: tactics.json)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new tactic to drill")
    p_add.add_argument("--fen", required=True, help="FEN of the tactic position")
    p_add.add_argument("--best-move", required=True, help="Best move for the position (SAN or UCI)")
    p_add.add_argument("--theme", default="", help="Tactic theme (e.g. fork, pin)")
    p_add.add_argument("--difficulty", default="", help="Difficulty (e.g. beginner, intermediate)")

    sub.add_parser("list", help="List all tactics")

    p_show = sub.add_parser("show", help="Show details of one tactic")
    p_show.add_argument("id", help="Tactic ID")

    p_solve = sub.add_parser("solve", help="Drill a single tactic")
    p_solve.add_argument("id", help="Tactic ID")

    sub.add_parser("quiz", help="Run the tactics quiz")

    sub.add_parser("stats", help="Show overall accuracy and streak statistics")

    p_delete = sub.add_parser("delete", help="Delete a tactic")
    p_delete.add_argument("id", help="Tactic ID")
    return parser


def cmd_add(args: argparse.Namespace, storage: Storage) -> int:
    fen = args.fen
    if not validate_fen(fen):
        print(f"Error: invalid FEN: {fen}", file=sys.stderr)
        return 1

    try:
        import chess

        board = chess.Board(fen)
        try:
            board.parse_san(args.best_move)
        except ValueError:
            try:
                board.parse_uci(args.best_move)
            except ValueError:
                print(
                    f"Error: invalid move '{args.best_move}' for FEN {fen}",
                    file=sys.stderr,
                )
                return 1
    except ImportError:
        pass

    tactic = Tactic.new(
        fen=fen,
        best_move=args.best_move,
        theme=args.theme,
        difficulty=args.difficulty,
    )
    storage.add(tactic)
    print(
        f"Added tactic {tactic.id} [theme={args.theme or '-'} difficulty={args.difficulty or '-'}]"
    )
    return 0


def cmd_list(args: argparse.Namespace, storage: Storage) -> int:
    tactics = storage.load()
    if not tactics:
        print("No tactics yet.")
        return 0
    for tactic in tactics:
        print(
            f"{tactic.id}  {tactic.created_at[:10]}  "
            f"{tactic.difficulty or '-'}  {tactic.theme or '-'}  "
            f"attempts={tactic.attempts} correct={tactic.correct} "
            f"accuracy={tactic.accuracy:.0f}% streak={tactic.streak}"
        )
    return 0


def _show_tactic(tactic: Tactic) -> None:
    print(f"ID:        {tactic.id}")
    print(f"Created:   {tactic.created_at}")
    print(f"Theme:     {tactic.theme or '-'}")
    print(f"Difficulty:{tactic.difficulty or '-'}")
    print(f"Best move: {tactic.best_move}")
    print(
        f"Attempts:  {tactic.attempts}  Correct: {tactic.correct}  Accuracy: {tactic.accuracy:.0f}%"
    )
    print(f"Streak:    {tactic.streak}  Best streak: {tactic.best_streak}")
    print(f"Last attempted: {tactic.last_attempted or '-'}")
    print(f"Solved at:  {tactic.solved_at or '-'}")
    print()
    if validate_fen(tactic.fen):
        print(board_ascii(tactic.fen))
    else:
        print(f"(invalid FEN: {tactic.fen})")


def cmd_show(args: argparse.Namespace, storage: Storage) -> int:
    tactic = storage.find(args.id)
    if tactic is None:
        print(f"Tactic not found: {args.id}", file=sys.stderr)
        return 1
    _show_tactic(tactic)
    return 0


def cmd_solve(args: argparse.Namespace, storage: Storage) -> int:
    tactic = storage.find(args.id)
    if tactic is None:
        print(f"Tactic not found: {args.id}", file=sys.stderr)
        return 1
    print(board_ascii(tactic.fen))
    print(f"Theme: {tactic.theme or '-'}  Difficulty: {tactic.difficulty or '-'}")
    try:
        answer = input("Best move: ").strip()
    except EOFError:
        print()
        return 0
    if not answer:
        print("No move entered.")
        return 0
    ok, feedback = check_move(tactic.fen, answer, tactic.best_move)
    now = datetime.now(timezone.utc).isoformat()
    tactic.attempts += 1
    tactic.last_attempted = now
    if ok:
        tactic.correct += 1
        tactic.streak += 1
        tactic.best_streak = max(tactic.best_streak, tactic.streak)
        if not tactic.solved_at:
            tactic.solved_at = now
    else:
        tactic.streak = 0
    storage.update(tactic)
    print()
    print(feedback)
    print(
        f"Accuracy: {tactic.accuracy:.0f}%  Streak: {tactic.streak}  "
        f"Best streak: {tactic.best_streak}"
    )
    return 0


def _quiz_loop(tactics: list[Tactic]) -> tuple[int, int, ScoreTracker]:
    remaining = list(tactics)
    unsolved = [t for t in remaining if not t.solved]
    solved = [t for t in remaining if t.solved]
    random.shuffle(unsolved)
    random.shuffle(solved)
    order = unsolved + solved

    tracker = ScoreTracker()
    correct = 0
    total = 0
    for tactic in order:
        print(board_ascii(tactic.fen))
        print(
            f"Theme: {tactic.theme or '-'}  Difficulty: {tactic.difficulty or '-'}  "
            f"({total + 1}/{len(order)})"
        )
        try:
            answer = input("Best move (or 'q' to quit): ").strip()
        except EOFError:
            print()
            break
        if answer.lower() in ("q", "quit"):
            break
        if not answer:
            print("Skipping.")
            print()
            continue
        ok, feedback = check_move(tactic.fen, answer, tactic.best_move)
        now = datetime.now(timezone.utc).isoformat()
        tactic.attempts += 1
        tactic.last_attempted = now
        tracker.record(ok)
        total += 1
        if ok:
            tactic.correct += 1
            correct += 1
            tactic.streak += 1
            tactic.best_streak = max(tactic.best_streak, tactic.streak)
            if not tactic.solved_at:
                tactic.solved_at = now
        else:
            tactic.streak = 0
        print(feedback)
        print(
            f"Accuracy: {tracker.accuracy:.1f}%  Streak: {tracker.streak}  "
            f"Best: {tracker.best_streak}"
        )
        print()
    return correct, total, tracker


def cmd_quiz(args: argparse.Namespace, storage: Storage) -> int:
    tactics = storage.load()
    if not tactics:
        print("No tactics to quiz yet. Add some with `add`.")
        return 0
    correct, total, tracker = _quiz_loop(tactics)
    storage.save(tactics)
    print("Quiz over.")
    print(
        f"Result: {correct}/{total} correct, "
        f"accuracy {tracker.accuracy:.1f}%, "
        f"best streak {tracker.best_streak}"
    )
    return 0


def cmd_stats(args: argparse.Namespace, storage: Storage) -> int:
    tactics = storage.load()
    total_tactics = len(tactics)
    attempts = sum(t.attempts for t in tactics)
    correct = sum(t.correct for t in tactics)
    solved = sum(1 for t in tactics if t.solved)
    best_streak = max((t.best_streak for t in tactics), default=0)
    tracker = ScoreTracker(attempts=attempts, correct=correct, best_streak=best_streak)
    print(f"Total tactics: {total_tactics}")
    print(f"Solved at least once: {solved}")
    print(f"Total attempts: {attempts}")
    print(f"Overall accuracy: {tracker.accuracy:.1f}%")
    print(f"Best streak across tactics: {best_streak}")
    return 0


def cmd_delete(args: argparse.Namespace, storage: Storage) -> int:
    if storage.delete(args.id):
        print(f"Deleted tactic {args.id}")
        return 0
    print(f"Tactic not found: {args.id}", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    storage = Storage(args.storage)
    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "show": cmd_show,
        "solve": cmd_solve,
        "quiz": cmd_quiz,
        "stats": cmd_stats,
        "delete": cmd_delete,
    }
    return commands[args.command](args, storage)


if __name__ == "__main__":
    raise SystemExit(main())
