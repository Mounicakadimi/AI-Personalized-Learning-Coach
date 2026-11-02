
import streamlit as st
import json
import sqlite3
import pandas as pd

from database import initialize_database
from learning_plan import create_learning_plan
from quiz_manager import generate_quiz, evaluate_quiz

DB_NAME = "learning_coach.db"

st.set_page_config(
    page_title="AI Personalized Learning Coach",
    page_icon="🎓",
    layout="wide"
)

initialize_database()


def save_learner(name, subject, goal, level, duration, daily_minutes):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO learners
        (name, subject, learning_goal, level, duration, daily_minutes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, subject, goal, level, duration, daily_minutes))

    learner_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return learner_id


def save_plan(learner_id, plan):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO learning_plans (learner_id, plan_content)
        VALUES (?, ?)
    """, (learner_id, json.dumps(plan)))

    conn.commit()
    conn.close()


def save_quiz_attempt(learner_id, subject, score, total):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO quiz_attempts
        (learner_id, subject, score, total_questions)
        VALUES (?, ?, ?, ?)
    """, (learner_id, subject, score, total))

    conn.commit()
    conn.close()


def get_dashboard_data():
    conn = sqlite3.connect(DB_NAME)

    learners = pd.read_sql_query(
        "SELECT * FROM learners", conn
    )

    plans = pd.read_sql_query(
        "SELECT * FROM learning_plans", conn
    )

    attempts = pd.read_sql_query(
        "SELECT * FROM quiz_attempts", conn
    )

    conn.close()

    return learners, plans, attempts


# Session State
if "learner_id" not in st.session_state:
    st.session_state.learner_id = None

if "learning_plan" not in st.session_state:
    st.session_state.learning_plan = None

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = None

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None


# Sidebar Navigation
st.sidebar.title("🎓 Learning Coach")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Create Learning Plan",
        "Study Plan",
        "Practice Quiz",
        "Progress Dashboard"
    ]
)


# HOME PAGE
if page == "Home":

    st.title("🎓 AI Personalized Learning Coach")

    st.subheader("Your personal AI-powered learning assistant")

    st.write("""
    This application helps learners create personalized learning plans,
    practice with AI-generated quizzes, evaluate their performance,
    and track their learning progress.
    """)

    col1, col2, col3 = st.columns(3)

    col1.info("📚 Personalized Learning Plans")
    col2.info("🧠 AI-Generated Quizzes")
    col3.info("📊 Progress Tracking")

    st.markdown("---")

    st.subheader("How to use the application")

    st.write("""
    1. Create your personalized learning plan.
    2. View your day-wise study schedule.
    3. Practice quizzes based on your subject.
    4. Check your quiz score and feedback.
    5. Track your progress in the dashboard.
    """)


# CREATE LEARNING PLAN
elif page == "Create Learning Plan":

    st.title("📚 Create Your Learning Plan")

    with st.form("learning_plan_form"):

        name = st.text_input("Learner Name")

        subject = st.text_input(
            "Subject",
            placeholder="Example: Python Programming"
        )

        goal = st.text_input(
            "Learning Goal",
            placeholder="Example: Learn Python and build projects"
        )

        level = st.selectbox(
            "Current Skill Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

        duration = st.number_input(
            "Duration (Days)",
            min_value=1,
            max_value=30,
            value=7
        )

        daily_minutes = st.number_input(
            "Daily Study Time (Minutes)",
            min_value=15,
            max_value=300,
            value=60
        )

        submit = st.form_submit_button("Generate Learning Plan")

    if submit:

        if not name.strip() or not subject.strip() or not goal.strip():
            st.error("Please fill in all required fields.")

        else:

            with st.spinner("Generating your personalized learning plan..."):

                try:

                    learner_id = save_learner(
                        name,
                        subject,
                        goal,
                        level,
                        int(duration),
                        int(daily_minutes)
                    )

                    plan = create_learning_plan(
                        subject,
                        goal,
                        level,
                        int(duration),
                        int(daily_minutes)
                    )

                    save_plan(learner_id, plan)

                    st.session_state.learner_id = learner_id
                    st.session_state.learning_plan = plan

                    st.session_state.quiz_questions = None
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_result = None

                    st.success("Learning plan generated successfully!")

                    st.json(plan)

                except Exception as error:
                    st.error(f"Error generating plan: {error}")


# STUDY PLAN
elif page == "Study Plan":

    st.title("📖 Your Study Plan")

    plan = st.session_state.learning_plan

    if plan is None:

        st.warning(
            "Please create a learning plan first from the Create Learning Plan page."
        )

    else:

        st.subheader(f"Subject: {plan['subject']}")

        st.write(f"Learning Goal: {plan['goal']}")
        st.write(f"Level: {plan['level']}")
        st.write(f"Duration: {plan['duration']} days")
        st.write(f"Daily Study Time: {plan['daily_minutes']} minutes")

        st.markdown("---")

        for day in plan["plan"]:

            with st.expander(f"Day {day['day']}: {day['topic']}"):

                st.write("### Description")
                st.write(day["description"])

                st.write("### Practice Activity")
                st.write(day["activity"])

                st.write("### Expected Outcome")
                st.write(day["expected_outcome"])


# PRACTICE QUIZ
elif page == "Practice Quiz":

    st.title("🧠 Practice Quiz")

    plan = st.session_state.learning_plan

    if plan is None:

        st.warning(
            "Please create a learning plan before practicing the quiz."
        )

    else:

        topics = [day["topic"] for day in plan["plan"]]

        selected_topic = st.selectbox("Select a topic", topics)

        if st.button("Generate Quiz"):

            with st.spinner("Generating quiz questions..."):

                try:

                    questions = generate_quiz(
                        plan["subject"],
                        selected_topic,
                        plan["level"]
                    )

                    st.session_state.quiz_questions = questions
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_result = None
                    st.session_state.quiz_topic = selected_topic

                except Exception as error:
                    st.error(f"Quiz generation failed: {error}")

        questions = st.session_state.quiz_questions

        if questions is not None:

            st.subheader(f"Quiz Topic: {st.session_state.quiz_topic}")

            if not st.session_state.quiz_submitted:

                with st.form("quiz_form"):

                    user_answers = {}

                    for index, question in enumerate(questions):

                        st.write(f"### Question {index + 1}")
                        st.write(question["question"])

                        options = question["options"]

                        selected_option = st.radio(
                            f"Choose your answer for Question {index + 1}",
                            list(options.keys()),
                            format_func=lambda option: (
                                f"{option}. {options[option]}"
                            ),
                            key=f"question_{index}"
                        )

                        user_answers[index] = selected_option

                    submitted = st.form_submit_button("Submit Quiz")

                if submitted:

                    result = evaluate_quiz(
                        questions,
                        user_answers
                    )

                    st.session_state.quiz_result = result
                    st.session_state.quiz_submitted = True

                    if st.session_state.learner_id is not None:

                        save_quiz_attempt(
                            st.session_state.learner_id,
                            plan["subject"],
                            result["score"],
                            result["total"]
                        )

                    st.rerun()

            else:

                result = st.session_state.quiz_result

                st.subheader("Quiz Results")

                st.metric(
                    "Your Score",
                    f"{result['score']} / {result['total']}"
                )

                st.metric(
                    "Percentage",
                    f"{result['percentage']:.2f}%"
                )

                st.success(result["recommendation"])

                st.markdown("---")

                st.subheader("Answer Feedback")

                for index, feedback in enumerate(result["feedback"]):

                    st.write(f"### Question {index + 1}")
                    st.write(feedback["question"])

                    if feedback["is_correct"]:
                        st.success("Correct Answer!")
                    else:
                        st.error("Incorrect Answer")

                    st.write(f"Your Answer: {feedback['your_answer']}")
                    st.write(f"Correct Answer: {feedback['correct_answer']}")
                    st.write(f"Explanation: {feedback['explanation']}")

                if st.button("Try Another Quiz"):

                    st.session_state.quiz_questions = None
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_result = None

                    st.rerun()


# PROGRESS DASHBOARD
elif page == "Progress Dashboard":

    st.title("📊 Progress Dashboard")

    learners, plans, attempts = get_dashboard_data()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Learners", len(learners))
    col2.metric("Learning Plans Created", len(plans))
    col3.metric("Quiz Attempts", len(attempts))

    st.markdown("---")

    if not attempts.empty:

        attempts["percentage"] = (
            attempts["score"] /
            attempts["total_questions"] * 100
        )

        st.subheader("Quiz Performance")

        st.line_chart(attempts["percentage"])

        st.subheader("Quiz History")

        st.dataframe(attempts, use_container_width=True)

        average_score = attempts["percentage"].mean()

        st.metric(
            "Average Quiz Score",
            f"{average_score:.2f}%"
        )

    else:

        st.info(
            "No quiz attempts recorded yet. Practice a quiz to see your progress."
        )

    st.markdown("---")

    st.subheader("Learner Information")

    if not learners.empty:

        st.dataframe(
            learners,
            use_container_width=True
        )

    else:

        st.info("No learners registered yet.")
