"""Quiz mode: drill tactics and report accuracy and streaks."""

from __future__ import annotations

import random

from .models import Tactic


def check_move(fen: str, move_text: str, best_move: str) -> tuple[bool, str]:
    """Check ``move_text`` against the tactic's best move.

    Returns ``(correct, feedback)``. SAN and UCI are both accepted.
    """
    import chess

    board = chess.Board(fen)
    try:
        move = board.parse_san(move_text)
    except ValueError:
        try:
            move = board.parse_uci(move_text)
        except ValueError:
            return False, f"Invalid move '{move_text}'."
    user_san = board.san(move)

    try:
        best = board.parse_san(best_move)
        best_san = board.san(best)
    except ValueError:
        best_san = best_move

    if user_san == best_san:
        return True, f"Correct! {user_san} is the best move."
    return False, f"Not quite. The best move is {best_san}."


def pick_quiz_tactic(tactics: list[Tactic]) -> Tactic | None:
    """Pick the next tactic to quiz: unsolved first, then least attempted."""
    if not tactics:
        return None
    unsolved = [t for t in tactics if not t.solved]
    pool = unsolved if unsolved else tactics
    ordered = sorted(pool, key=lambda t: t.attempts)
    top = ordered[: max(1, len(ordered) // 3)] or ordered
    return random.choice(top)
