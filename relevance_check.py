import openai
from sklearn.metrics.pairwise import cosine_similarity

def get_embedding(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(input=text, model=model)
    return response["data"][0]["embedding"]

def calculate_semantic_similarity(course_material, generated_content):
    """Calculate semantic similarity between course material and generated content."""
    try:
        course_embedding = get_embedding(course_material)
        generated_embedding = get_embedding(generated_content)
        similarity = cosine_similarity([course_embedding], [generated_embedding])[0][0]
        return round(similarity, 3)
    except Exception as e:
        print(f"Error calculating semantic similarity: {e}")
        return None

import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    """Extract keywords from a given text using spaCy."""
    doc = nlp(text)
    return {token.text.lower() for token in doc if token.is_alpha and not token.is_stop}

def calculate_keyword_overlap(course_material, generated_content):
    """Calculate the percentage overlap of keywords between course material and generated content."""
    try:
        course_keywords = extract_keywords(course_material)
        generated_keywords = extract_keywords(generated_content)
        overlap = course_keywords.intersection(generated_keywords)
        return round(len(overlap) / len(course_keywords), 3) if course_keywords else 0.0
    except Exception as e:
        print(f"Error calculating keyword overlap: {e}")
        return None

def calculate_feedback_score(course_material, generated_content):
    """Get relevance feedback from the LLM."""
    feedback_prompt = f"""
    You are an evaluator. Compare the following generated content with the original course material.
    Provide a relevance score between 0 (not relevant) to 10 (highly relevant), and explain why.

    Course Material:
    {course_material}

    Generated Content:
    {generated_content}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an evaluator who provides feedback on content relevance."},
                {"role": "user", "content": feedback_prompt}
            ]
        )
        feedback_response = response["choices"][0]["message"]["content"]
        # Extract numeric score from the response
        score = [int(s) for s in feedback_response.split() if s.isdigit()]
        return score[0] if score else None, feedback_response
    except Exception as e:
        print(f"Error in feedback loop: {e}")
        return None, "Failed to get feedback."
