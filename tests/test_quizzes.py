import pytest
from quiz_handler import generate_quiz, evaluate_quiz

def test_generate_quiz():
    """Test quiz generation based on text."""
    content = "Machine learning involves supervised and unsupervised learning."
    quiz, answers = generate_quiz(content, "easy")
    assert len(quiz) > 0
    assert len(answers) > 0

def test_evaluate_quiz():
    """Test quiz evaluation."""
    submitted_answers = {0: "A", 1: "True"}
    correct_answers = {0: "A", 1: "True"}
    score, total, _ = evaluate_quiz(submitted_answers, correct_answers)
    assert score == 2
    assert total == 2
