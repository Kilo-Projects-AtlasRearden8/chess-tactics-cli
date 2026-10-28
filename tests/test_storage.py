"""Tests for atomic JSON storage."""

from chess_tactics.models import Tactic
from chess_tactics.storage import Storage


def _sample() -> Tactic:
    return Tactic.new(
        fen="rnbqkbnr/pppppppp/8/8/4N3/8/PPPPPPPP/RNBQKB1R b KQkq - 1 3",
        best_move="Nf3",
        theme="fork",
        difficulty="beginner",
    )


def test_load_missing_file_returns_empty(tmp_path):
    storage = Storage(tmp_path / "missing.json")
    assert storage.load() == []


def test_add_load_delete_roundtrip(tmp_path):
    storage = Storage(tmp_path / "tactics.json")
    tactic = _sample()
    storage.add(tactic)

    loaded = storage.load()
    assert len(loaded) == 1
    assert loaded[0].id == tactic.id
    assert loaded[0].fen == tactic.fen

    found = storage.find(tactic.id)
    assert found is not None
    assert found.theme == "fork"

    assert storage.delete(tactic.id) is True
    assert storage.find(tactic.id) is None
    assert storage.delete(tactic.id) is False
    assert storage.load() == []


def test_update_tactic(tmp_path):
    storage = Storage(tmp_path / "tactics.json")
    tactic = _sample()
    storage.add(tactic)

    tactic.attempts = 5
    tactic.correct = 4
    assert storage.update(tactic) is True

    loaded = storage.load()
    assert len(loaded) == 1
    assert loaded[0].attempts == 5
    assert loaded[0].correct == 4
    assert loaded[0].accuracy == 80.0

    missing = Tactic.new(fen="8/8/8/8/8/8/8/8 w - - 0 1", best_move="e4")
    assert storage.update(missing) is False


def test_save_writes_valid_json_and_no_tmp_leftovers(tmp_path):
    storage = Storage(tmp_path / "tactics.json")
    storage.add(_sample())

    files = [p.name for p in tmp_path.iterdir()]
    assert "tactics.json" in files
    assert not any(name.endswith(".tmp") for name in files)

    import json

    with (tmp_path / "tactics.json").open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert data[0]["id"] == storage.load()[0].id


def test_corrupt_file_returns_empty(tmp_path):
    storage = Storage(tmp_path / "tactics.json")
    storage.path.write_text("{not valid json", encoding="utf-8")
    assert storage.load() == []


def test_non_list_json_returns_empty(tmp_path):
    storage = Storage(tmp_path / "tactics.json")
    storage.path.write_text('{"not": "a list"}', encoding="utf-8")
    assert storage.load() == []
