"""Tests for scoring: accuracy and streaks."""

from chess_tactics.scoring import ScoreTracker


def test_new_tracker_has_zero_stats():
    tracker = ScoreTracker()
    assert tracker.attempts == 0
    assert tracker.correct == 0
    assert tracker.streak == 0
    assert tracker.best_streak == 0
    assert tracker.accuracy == 0.0


def test_correct_updates_accuracy_and_streak():
    tracker = ScoreTracker()
    tracker.record(True)
    assert tracker.attempts == 1
    assert tracker.correct == 1
    assert tracker.streak == 1
    assert tracker.best_streak == 1
    assert tracker.accuracy == 100.0

    tracker.record(True)
    assert tracker.attempts == 2
    assert tracker.streak == 2
    assert tracker.best_streak == 2
    assert tracker.accuracy == 100.0


def test_incorrect_resets_streak_but_keeps_best():
    tracker = ScoreTracker()
    tracker.record(True)
    tracker.record(True)
    tracker.record(False)
    assert tracker.attempts == 3
    assert tracker.correct == 2
    assert tracker.streak == 0
    assert tracker.best_streak == 2
    assert abs(tracker.accuracy - (2 / 3) * 100) < 1e-9


def test_best_streak_tracks_maximum():
    tracker = ScoreTracker(attempts=0, correct=0, streak=0, best_streak=3)
    tracker.record(False)  # streak 0, best stays 3
    assert tracker.best_streak == 3
    tracker.record(True)
    tracker.record(True)
    assert tracker.streak == 2
    assert tracker.best_streak == 3
    tracker.record(True)
    assert tracker.best_streak == 3

    tracker2 = ScoreTracker()
    for correct in [True, True, True, False, True, True]:
        tracker2.record(correct)
    assert tracker2.best_streak == 3


def test_from_fields_restores_state():
    tracker = ScoreTracker(attempts=10, correct=7, streak=2, best_streak=5)
    assert tracker.accuracy == 70.0
