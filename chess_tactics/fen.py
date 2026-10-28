"""FEN validation and board rendering."""

from __future__ import annotations

import chess


def validate_fen(fen: str) -> bool:
    """Return True if ``fen`` is a position FEN accepted by python-chess."""
    try:
        chess.Board(fen)
        return True
    except ValueError:
        return False


def board_from_fen(fen: str) -> chess.Board:
    """Return a :class:`chess.Board` for ``fen`` (raises ValueError if invalid)."""
    return chess.Board(fen)


def board_ascii(fen: str) -> str:
    """Return an ASCII rendering of the position described by ``fen``."""
    board = board_from_fen(fen)
    lines: list[str] = []
    for rank in range(8, 0, -1):
        row = []
        for file in range(8):
            piece = board.piece_at(chess.square(file, rank - 1))
            row.append(piece.symbol() if piece else ".")
        lines.append(" ".join(row))
    turn = "White" if board.turn == chess.WHITE else "Black"
    lines.append(f"Turn: {turn}")
    return "\n".join(lines)
