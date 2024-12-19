from quiz_handler import evaluate_quiz

def test_evaluate_quiz_correct():
    """Test evaluating a quiz with all correct answers."""
    submitted_answers = {0: "A", 1: "True", 2: ["A", "C"]}
    correct_answers = {0: "A", 1: "True", 2: ["A", "C"]}
    score, total, feedback = evaluate_quiz(submitted_answers, correct_answers)
    assert score == 3
    assert total == 3
    assert "Correct" in feedback[0]

def test_evaluate_quiz_incorrect():
    """Test evaluating a quiz with some incorrect answers."""
    submitted_answers = {0: "B", 1: "False", 2: ["A"]}
    correct_answers = {0: "A", 1: "True", 2: ["A", "C"]}
    score, total, feedback = evaluate_quiz(submitted_answers, correct_answers)
    assert score == 1
    assert total == 3
    assert "Incorrect" in feedback[0]
