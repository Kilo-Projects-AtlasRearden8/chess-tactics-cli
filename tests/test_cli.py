"""Tests for the CLI."""

from chess_tactics.cli import main

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_add_invalid_fen_rejected(capsys):
    code = main(["add", "--fen", "not-a-fen", "--best-move", "e4"])
    assert code == 1
    assert "invalid FEN" in capsys.readouterr().err


def test_add_valid_tactic(tmp_path, monkeypatch, capsys):
    storage_file = tmp_path / "tactics.json"
    code = main(
        [
            "--storage",
            str(storage_file),
            "add",
            "--fen",
            STARTING_FEN,
            "--best-move",
            "e4",
            "--theme",
            "opening",
            "--difficulty",
            "beginner",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "Added tactic" in out


def test_list_and_stats(tmp_path, capsys):
    storage_file = tmp_path / "tactics.json"
    main(["--storage", str(storage_file), "add", "--fen", STARTING_FEN, "--best-move", "e4"])
    from chess_tactics.storage import Storage

    tactic_id = Storage(storage_file).load()[0].id
    code = main(["--storage", str(storage_file), "list"])
    assert code == 0
    out = capsys.readouterr().out
    assert tactic_id in out

    code = main(["--storage", str(storage_file), "stats"])
    assert code == 0
    assert "Total tactics:" in capsys.readouterr().out


def test_show_and_delete_missing(tmp_path, capsys):
    storage_file = tmp_path / "tactics.json"
    code = main(["--storage", str(storage_file), "show", "nope"])
    assert code == 1
    assert "Tactic not found" in capsys.readouterr().err

    code = main(["--storage", str(storage_file), "delete", "nope"])
    assert code == 1


def test_quiz_empty(tmp_path, capsys):
    storage_file = tmp_path / "tactics.json"
    code = main(["--storage", str(storage_file), "quiz"])
    assert code == 0
    assert "No tactics to quiz yet" in capsys.readouterr().out


def test_solve_correct_and_incorrect(tmp_path, monkeypatch, capsys):
    storage_file = tmp_path / "tactics.json"
    main(
        [
            "--storage",
            str(storage_file),
            "add",
            "--fen",
            STARTING_FEN,
            "--best-move",
            "e4",
        ]
    )
    # find the added id via the loaded storage is not needed; use solve with
    # a guessed id would be fragile, so instead add then list to learn id.
    from chess_tactics.storage import Storage

    tactic_id = Storage(storage_file).load()[0].id

    monkeypatch.setattr("builtins.input", lambda prompt="": "e4")
    code = main(["--storage", str(storage_file), "solve", tactic_id])
    assert code == 0
    out = capsys.readouterr().out
    assert "Correct!" in out
    assert "Accuracy: 100%" in out

    monkeypatch.setattr("builtins.input", lambda prompt="": "d4")
    code = main(["--storage", str(storage_file), "solve", tactic_id])
    assert code == 0
    out = capsys.readouterr().out
    assert "Not quite" in out
    assert "Accuracy: 50%" in out
