
import sqlite3

DB_NAME = "learning_coach.db"


def initialize_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learners (
            learner_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            learning_goal TEXT NOT NULL,
            level TEXT NOT NULL,
            duration INTEGER,
            daily_minutes INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_plans (
            plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_id INTEGER,
            plan_content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (learner_id) REFERENCES learners(learner_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_id INTEGER,
            subject TEXT,
            score INTEGER,
            total_questions INTEGER,
            attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (learner_id) REFERENCES learners(learner_id)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")
