import pytest
from unittest.mock import patch
from relevance_check import calculate_semantic_similarity, calculate_keyword_overlap, calculate_feedback_score

# Test Semantic Similarity
def test_calculate_semantic_similarity():
    course_material = "Machine learning involves algorithms for data analysis."
    generated_content = "Data analysis is a key part of machine learning."

    with patch("relevance_check.get_embedding", side_effect=[
        [0.1, 0.2, 0.3],  # Mock embedding for course_material
        [0.1, 0.2, 0.3]   # Mock embedding for generated_content
    ]):
        similarity = calculate_semantic_similarity(course_material, generated_content)
        assert similarity == 1.0

def test_calculate_semantic_similarity_no_match():
    course_material = "Machine learning involves algorithms for data analysis."
    generated_content = "The weather is sunny today."

    with patch("relevance_check.get_embedding", side_effect=[
        [0.1, 0.2, 0.3],  # Mock embedding for course_material
        [-0.4, -0.5, -0.6]   # Mock embedding for generated_content
    ]):
        similarity = calculate_semantic_similarity(course_material, generated_content)
        assert similarity < 0.3

# Test Keyword Overlap
def test_calculate_keyword_overlap():
    course_material = "Machine learning uses data analysis and algorithms."
    generated_content = "Data analysis and algorithms are important."

    overlap_score = calculate_keyword_overlap(course_material, generated_content)
    assert overlap_score == 0.5

def test_calculate_keyword_overlap_no_overlap():
    course_material = "Machine learning uses data analysis and algorithms."
    generated_content = "Weather patterns involve rain and sunshine."

    overlap_score = calculate_keyword_overlap(course_material, generated_content)
    assert overlap_score == 0.0

# Test LLM Feedback Score
def test_calculate_feedback_score():
    course_material = "Machine learning involves data analysis and algorithms."
    generated_content = "Data analysis and algorithms are vital for machine learning."

    feedback_mock_response = {
        "choices": [{
            "message": {
                "content": "Relevance Score: 9. The generated content is highly relevant."
            }
        }]
    }

    with patch("openai.ChatCompletion.create", return_value=feedback_mock_response):
        score, details = calculate_feedback_score(course_material, generated_content)
        assert score == 9
        assert "highly relevant" in details

def test_calculate_feedback_score_error():
    course_material = "Machine learning involves data analysis and algorithms."
    generated_content = "Data analysis and algorithms are vital for machine learning."

    with patch("openai.ChatCompletion.create", side_effect=Exception("API Error")):
        score, details = calculate_feedback_score(course_material, generated_content)
        assert score is None
        assert "Failed to get feedback" in details
