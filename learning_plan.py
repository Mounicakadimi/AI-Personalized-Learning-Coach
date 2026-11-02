
from ai_service import generate_json


def create_learning_plan(subject, goal, level, duration, daily_minutes):
    prompt = f"""
    You are an expert AI Personalized Learning Coach.

    Create a personalized learning plan using these details:

    Subject: {subject}
    Learning Goal: {goal}
    Skill Level: {level}
    Duration: {duration} days
    Daily Study Time: {daily_minutes} minutes

    Return ONLY valid JSON in this structure:

    {{
        "subject": "{subject}",
        "goal": "{goal}",
        "level": "{level}",
        "duration": {duration},
        "daily_minutes": {daily_minutes},
        "plan": [
            {{
                "day": 1,
                "topic": "Topic name",
                "description": "What the learner should study",
                "activity": "Practice activity",
                "expected_outcome": "What the learner will achieve"
            }}
        ]
    }}

    Create exactly {duration} days.
    Make the plan beginner-friendly, structured, practical, and progressive.
    """

    result = generate_json(prompt)

    if "plan" not in result:
        raise ValueError("Learning plan was not generated correctly.")

    if len(result["plan"]) != duration:
        raise ValueError("Generated plan does not contain the required number of days.")

    return result
