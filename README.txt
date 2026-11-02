


# AI Personalized Learning Coach

## Project Overview

AI Personalized Learning Coach is an AI-powered educational application designed to provide personalized learning experiences based on individual learner requirements, skill levels, learning goals, and available study time.

The system utilizes Google's Gemini AI to generate structured day-wise learning plans, create topic-based multiple-choice quizzes, evaluate learner performance, and provide personalized feedback. SQLite is used to store learner information, learning plans, and quiz attempts.

## Objectives

- Generate personalized learning plans.
- Adapt learning content based on skill level.
- Create AI-generated multiple-choice quizzes.
- Evaluate quiz answers and calculate scores.
- Identify weak topics and provide recommendations.
- Store learner data and assessment results.
- Monitor learning progress through a dashboard.

## Features

### 1. Personalized Learning Plan Generation
- Accepts learner name, subject, learning goal, skill level, duration, and daily study time.
- Generates a structured day-wise learning plan using Gemini AI.
- Provides topics, descriptions, activities, and expected outcomes.

### 2. Study Plan Management
- Displays the generated learning schedule.
- Organizes topics according to study days.
- Provides detailed learning activities and expected outcomes.

### 3. AI-Based Quiz Generation
- Generates five multiple-choice questions for a selected topic.
- Includes four answer options per question.
- Provides correct answers and explanations.

### 4. Quiz Evaluation
- Evaluates learner responses using Python.
- Calculates total score and percentage.
- Provides answer-wise feedback.
- Recommends revision or progression based on performance.

### 5. Progress Dashboard
- Displays total learners.
- Displays learning plans created.
- Tracks quiz attempts.
- Calculates average quiz performance.
- Displays quiz history and learner information.

### 6. Database Management
- Stores learner information in SQLite.
- Stores generated learning plans.
- Stores quiz scores and assessment attempts.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development and evaluation logic |
| Streamlit | Interactive web application interface |
| Google Gemini API | AI-based learning plan and quiz generation |
| SQLite | Database management |
| Pandas | Data processing and dashboard visualization |
| python-dotenv | Environment variable management |
| Git | Version control |
| GitHub | Source code repository |

## Project Architecture

Learner Input
    |
    v
Streamlit User Interface
    |
    v
Python Application Logic
    |
    +----------------------+
    |                     |
    v                     v
Google Gemini API       SQLite Database
    |                     |
    v                     v
Learning Plans        Learner Records
AI Quizzes           Learning Plans
AI Feedback          Quiz Attempts
    |
    v
Quiz Evaluation
    |
    v
Progress Dashboard

## Project Structure

ai-personalized-learning-coach/
│
├── app.py
├── database.py
├── ai_service.py
├── learning_plan.py
├── quiz_manager.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-personalized-learning-coach.git
```

### Step 2: Navigate to the Project Directory

```bash
cd ai-personalized-learning-coach
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure Gemini API

Create a `.env` file in the project directory.

Add the following configuration:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-flash-latest
```

Replace `your_gemini_api_key` with your actual Gemini API key.

### Step 7: Initialize the Database

```bash
python database.py
```

### Step 8: Run the Application

```bash
streamlit run app.py
```

The application will open in the browser.

## Application Modules

### app.py
Main Streamlit application responsible for navigation, learner input, learning plan display, quiz interaction, and dashboard visualization.

### database.py
Handles SQLite database initialization and table creation.

### ai_service.py
Establishes communication with the Google Gemini API and processes JSON responses.

### learning_plan.py
Generates personalized day-wise learning plans based on learner requirements.

### quiz_manager.py
Generates topic-based quizzes, evaluates answers, calculates scores, and provides performance recommendations.

## Database Design

### Learners Table
Stores learner details, including name, subject, learning goal, skill level, duration, and daily study time.

### Learning Plans Table
Stores generated learning plan content associated with learners.

### Quiz Attempts Table
Stores learner quiz scores, total questions, subject, and attempt timestamps.

## Expected Outcomes

- Improved learning organization through personalized study schedules.
- Efficient topic-wise knowledge assessment.
- Automated quiz evaluation.
- Performance-based learning recommendations.
- Persistent storage of learner and assessment data.
- Improved visibility into learning progress.

## Future Enhancements

- User authentication and profile management.
- Topic completion tracking.
- Advanced performance analytics.
- Weak-topic identification and adaptive learning.
- Downloadable learning plans in PDF format.
- Integration of additional AI models.
- Responsive UI enhancements.
- Learning streaks and gamification.

## Security

- API keys are stored using environment variables.
- The `.env` file is excluded from version control.
- Database operations use parameterized SQL queries.
- Sensitive configuration values must not be committed to GitHub.

## Conclusion

AI Personalized Learning Coach provides an intelligent and interactive learning environment by integrating generative AI, Python-based assessment logic, and database-driven progress tracking. The application supports personalized learning plan generation, automated quiz evaluation, and learner performance monitoring.

## Author

AI Engineering Internship Project

## License

This project is developed for educational and internship purposes.
