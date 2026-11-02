
from ai_service import generate_json


def generate_quiz(subject, topic, level):
    prompt = f"""
    Create exactly 5 multiple-choice quiz questions.

    Subject: {subject}
    Topic: {topic}
    Level: {level}

    Return valid JSON in this format:

    {{
        "questions": [
            {{
                "question": "Question text",
                "options": {{
                    "A": "Option A",
                    "B": "Option B",
                    "C": "Option C",
                    "D": "Option D"
                }},
                "correct_answer": "A",
                "explanation": "Explanation of the correct answer",
                "topic": "{topic}"
            }}
        ]
    }}

    Rules:
    - Exactly 5 questions.
    - Only one correct answer per question.
    - Keep questions suitable for the given level.
    - correct_answer must be A, B, C, or D.
    """

    result = generate_json(prompt)

    if "questions" not in result or len(result["questions"]) != 5:
        raise ValueError("Quiz must contain exactly 5 questions.")

    return result["questions"]


def evaluate_quiz(questions, user_answers):
    score = 0
    feedback = []

    for index, question in enumerate(questions):
        correct_answer = question["correct_answer"]
        user_answer = user_answers.get(index)

        is_correct = user_answer == correct_answer

        if is_correct:
            score += 1

        feedback.append({
            "question": question["question"],
            "your_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": question["explanation"],
            "topic": question["topic"]
        })

    percentage = (score / len(questions)) * 100 if questions else 0

    if percentage >= 80:
        recommendation = "Excellent! Move to the next topic."
    elif percentage >= 50:
        recommendation = "Good effort. Revise your weak topics."
    else:
        recommendation = "Review the topic and try the quiz again."

    return {
        "score": score,
        "total": len(questions),
        "percentage": percentage,
        "recommendation": recommendation,
        "feedback": feedback
    }
