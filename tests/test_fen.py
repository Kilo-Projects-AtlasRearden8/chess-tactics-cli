"""Tests for FEN parsing and board rendering."""

from chess_tactics.fen import board_ascii, board_from_fen, validate_fen

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_validate_fen_accepts_starting_position():
    assert validate_fen(STARTING_FEN) is True


def test_validate_fen_rejects_garbage():
    assert validate_fen("not-a-fen") is False
    assert validate_fen("") is False
    assert validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1") is False


def test_board_from_fen_sets_turn_and_move():
    board = board_from_fen(STARTING_FEN)
    assert board.turn is True  # White to move
    assert board.fullmove_number == 1

    black_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
    board = board_from_fen(black_fen)
    assert board.turn is False  # Black to move


def test_board_ascii_renders_pieces_and_turn():
    rendering = board_ascii(STARTING_FEN)
    assert "r" in rendering and "R" in rendering
    assert "Turn: White" in rendering

    black_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
    assert "Turn: Black" in board_ascii(black_fen)
