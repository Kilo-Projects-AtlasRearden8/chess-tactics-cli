"""Scoring: accuracy and streaks for tactic attempts."""

from __future__ import annotations


class ScoreTracker:
    """Tracks attempts, accuracy, current streak, and best streak."""

    def __init__(
        self,
        attempts: int = 0,
        correct: int = 0,
        streak: int = 0,
        best_streak: int = 0,
    ) -> None:
        self.attempts = attempts
        self.correct = correct
        self.streak = streak
        self.best_streak = best_streak

    def record(self, correct: bool) -> None:
        """Record one attempt and update accuracy and streaks."""
        self.attempts += 1
        if correct:
            self.correct += 1
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
        else:
            self.streak = 0

    @property
    def accuracy(self) -> float:
        """Percentage of correct attempts (0.0 when not attempted)."""
        if self.attempts == 0:
            return 0.0
        return 100.0 * self.correct / self.attempts
