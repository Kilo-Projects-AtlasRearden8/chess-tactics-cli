"""Atomic JSON storage for tactics."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from .models import Tactic


class Storage:
    """Read/write tactics to a local JSON file, written atomically."""

    def __init__(self, path: str | os.PathLike[str] = "tactics.json") -> None:
        self.path = Path(path)

    def load(self) -> list[Tactic]:
        """Load all tactics; returns an empty list for missing or bad files."""
        if not self.path.exists():
            return []
        try:
            with self.path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError):
            return []
        if not isinstance(data, list):
            return []
        tactics: list[Tactic] = []
        for item in data:
            try:
                tactics.append(Tactic.from_dict(item))
            except (KeyError, TypeError):
                continue
        return tactics

    def save(self, tactics: list[Tactic]) -> None:
        """Atomically write ``tactics`` to the storage file."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = [tactic.to_dict() for tactic in tactics]
        fd, tmp = tempfile.mkstemp(dir=str(self.path.parent), prefix=".tactics-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
            os.replace(tmp, self.path)
        except BaseException:
            try:
                os.remove(tmp)
            except OSError:
                pass
            raise

    def add(self, tactic: Tactic) -> None:
        tactics = self.load()
        tactics.append(tactic)
        self.save(tactics)

    def find(self, tactic_id: str) -> Tactic | None:
        for tactic in self.load():
            if tactic.id == tactic_id:
                return tactic
        return None

    def delete(self, tactic_id: str) -> bool:
        tactics = self.load()
        filtered = [t for t in tactics if t.id != tactic_id]
        if len(filtered) == len(tactics):
            return False
        self.save(filtered)
        return True

    def update(self, tactic: Tactic) -> bool:
        tactics = self.load()
        for index, existing in enumerate(tactics):
            if existing.id == tactic.id:
                tactics[index] = tactic
                self.save(tactics)
                return True
        return False
