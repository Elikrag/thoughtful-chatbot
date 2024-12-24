import os
import json
import math

from collections import Counter


SIMILARITY_THRESHOLD = 0.7
DEFAULT_RESPONSE = "Sorry, ThoughtfulBot does not have an answer to that question."


def load_question_answers():
    # Load the question and answer pairs from the question_answers.json file
    path = os.path.join(os.getcwd(), 'resources', 'question_answers.json')
    
    with open(path, 'r') as file:
        question_answers = json.load(file)

    return question_answers['questions']


def get_response(question: str, question_answers: dict) -> str:
    # Get the response to the user question 
    if question in question_answers:
        return question_answers[question]
    
    answer, similarity = fuzzy_match_question(question, question_answers)
    
    if similarity < SIMILARITY_THRESHOLD:
        return DEFAULT_RESPONSE

    return answer


def fuzzy_match_question(question: str, question_answers: dict) -> tuple[str, float]:
    # Find the most similar question in the question_answers using fuzzy matching
    similarities = []
    for q in question_answers:
        similarity = cosine_similarity(question, q["question"])
        similarities.append((q["answer"], similarity))
    
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    
    return similarities[0][0], similarities[0][1]


def cosine_similarity(s1: str, s2: str) -> float:
    # Calculate the cosine similarity between two strings
    c1 = Counter(s1.lower().split())
    c2 = Counter(s2.lower().split())
    terms = set(c1).union(c2)

    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)

    mag1 = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    mag2 = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))

    return dotprod / (mag1 * mag2)