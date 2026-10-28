"""Data models for chess tactics and their attempt statistics."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Tactic:
    """A single chess tactic: a FEN position with a known best move."""

    id: str
    fen: str
    best_move: str
    theme: str
    difficulty: str
    created_at: str
    attempts: int = 0
    correct: int = 0
    streak: int = 0
    best_streak: int = 0
    last_attempted: str | None = None
    solved_at: str | None = None

    @property
    def accuracy(self) -> float:
        """Percentage of correct attempts (0.0 when not attempted)."""
        if self.attempts == 0:
            return 0.0
        return 100.0 * self.correct / self.attempts

    @property
    def solved(self) -> bool:
        """True once the tactic has been answered correctly at least once."""
        return self.correct > 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "fen": self.fen,
            "best_move": self.best_move,
            "theme": self.theme,
            "difficulty": self.difficulty,
            "created_at": self.created_at,
            "attempts": self.attempts,
            "correct": self.correct,
            "streak": self.streak,
            "best_streak": self.best_streak,
            "last_attempted": self.last_attempted,
            "solved_at": self.solved_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Tactic:
        return cls(
            id=data["id"],
            fen=data["fen"],
            best_move=data["best_move"],
            theme=data.get("theme", ""),
            difficulty=data.get("difficulty", ""),
            created_at=data.get("created_at", ""),
            attempts=int(data.get("attempts", 0)),
            correct=int(data.get("correct", 0)),
            streak=int(data.get("streak", 0)),
            best_streak=int(data.get("best_streak", 0)),
            last_attempted=data.get("last_attempted"),
            solved_at=data.get("solved_at"),
        )

    @classmethod
    def new(
        cls,
        *,
        fen: str,
        best_move: str,
        theme: str = "",
        difficulty: str = "",
    ) -> Tactic:
        now = datetime.now(timezone.utc).isoformat()
        return cls(
            id=str(uuid.uuid4())[:8],
            fen=fen,
            best_move=best_move,
            theme=theme,
            difficulty=difficulty,
            created_at=now,
        )
