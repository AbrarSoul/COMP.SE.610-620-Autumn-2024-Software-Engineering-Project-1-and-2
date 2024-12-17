import openai
import json
import random

openai.api_key = "API KEY"

def generate_quiz(pdf_content, difficulty):
    """
    Generate quiz questions and answers in real-time using OpenAI API.

    Args:
        pdf_content (str): The text content extracted from the lecture PDF.
        difficulty (str): Selected difficulty level: 'easy', 'medium', or 'hard'.

    Returns:
        tuple: A list of question dictionaries and a dictionary of correct answers.
    """
    # Define the prompt for quiz generation
    prompt = f"""
    You are a helpful teaching assistant. Based on the following course material:
    {pdf_content}

    Generate a quiz with the following requirements:
    - Difficulty Level: {difficulty}
    - Question types:
      - 'easy': MCQ (single correct answer) and True/False questions only.
      - 'medium': Include MCQ (multiple correct answers).
      - 'hard': Generate more complex variations of MCQs and True/False questions.
    - Provide correct answers for each question.
    - Format questions as JSON in this structure:
      [
        {{
            "question": "Sample question text",
            "type": "mcq_single / mcq_multiple / true_false",
            "options": ["Option1", "Option2", "Option3"],
            "answer": "Correct answer or list of correct answers"
        }}
      ]
    """
    # Call OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        quiz_data = response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return [], {}

    # Convert response into Python objects
    try:
        quiz_questions = json.loads(quiz_data)
        correct_answers = {idx: q["answer"] for idx, q in enumerate(quiz_questions)}
        return quiz_questions, correct_answers
    except json.JSONDecodeError:
        print("Error parsing quiz data.")
        return [], {}


def evaluate_quiz(submitted_answers, correct_answers):
    """
    Evaluate submitted quiz answers.

    Args:
        submitted_answers (dict): Answers submitted by the student.
        correct_answers (dict): The correct answers for the quiz.

    Returns:
        tuple: Score, total questions, and detailed feedback.
    """
    score = 0
    total = len(correct_answers)
    feedback = {}

    for idx, correct in correct_answers.items():
        submitted = submitted_answers.get(idx, None)
        if isinstance(correct, list):
            # For MCQ (multiple answers), compare sets
            if set(submitted) == set(correct):
                score += 1
                feedback[idx] = "Correct"
            else:
                feedback[idx] = f"Incorrect. Correct answers: {', '.join(correct)}"
        else:
            # For MCQ (single answer) and True/False
            if submitted == correct:
                score += 1
                feedback[idx] = "Correct"
            else:
                feedback[idx] = f"Incorrect. Correct answer: {correct}"

    return score, total, feedback