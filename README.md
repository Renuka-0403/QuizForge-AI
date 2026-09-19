# QuizForge AI

## AI-Powered Adaptive Quiz Generator & Learning Assistant

QuizForge AI is an intelligent learning platform that transforms any subject, topic, study material, or PDF into an interactive and personalized quiz experience.

Instead of simply generating a fixed set of questions, QuizForge AI analyzes the learning material, creates questions across different difficulty levels and question types, evaluates the learner's performance, identifies weak areas, and adapts the quiz experience based on the learner's responses.

## Features

- Generate AI-powered multiple-choice questions from any subject or topic
- Generate quizzes from pasted study material
- Upload PDF study materials and automatically create quizzes
- Support up to 50 questions per quiz
- Choose from 5, 10, 15, 20, 30, 40, or 50 questions
- Select difficulty levels:
  - Easy
  - Medium
  - Hard
  - Adaptive
- Select question types:
  - Mixed
  - Concept Based
  - Application Based
  - Scenario Based
  - Code Based
- Practice Mode for learning and immediate feedback
- Exam Mode for test-style practice
- One-question-at-a-time interactive quiz interface
- Immediate answer feedback in Practice Mode
- AI-generated explanations for answers
- Automatic score calculation
- Accuracy analysis
- Weak-area detection
- Personalized AI learning analysis
- Practice weak areas again
- Adaptive difficulty that changes based on performance
- Question repetition prevention
- Quiz history tracking to reduce repeated questions
- Source-aware quiz generation
- Clean and modern educational interface
- Subject-independent design suitable for different fields of study

## Supported Subjects

QuizForge AI is designed to work with a wide range of subjects and educational domains.

Examples include:

- Computer Science
- Artificial Intelligence
- Data Science
- Mathematics
- Physics
- Chemistry
- Biology
- Medicine
- Environmental Science
- History
- Geography
- Economics
- Commerce
- Business Studies
- Psychology
- Law
- Engineering
- Management
- Fashion Designing
- Languages
- Literature
- General Knowledge
- And many other subjects

The system is not limited to computer science or technology-related topics.

## How It Works

QuizForge AI follows an intelligent quiz-generation workflow:

```text
User Input
    ↓
Topic / Study Material / PDF
    ↓
Material Analysis
    ↓
Subject Detection
    ↓
Question Blueprint Creation
    ↓
Difficulty & Question-Type Balancing
    ↓
AI Question Generation
    ↓
Question Validation
    ↓
Interactive Quiz
    ↓
Answer Evaluation
    ↓
Performance Analysis
    ↓
Weak Area Detection
    ↓
Adaptive Learning Recommendations
````

## Quiz Generation

The application can generate questions from three different sources.

### Topic

Enter a topic and let the AI create a quiz based on the selected settings.

### Study Material

Paste notes, textbook content, classroom material, or other study content directly into the application.

### PDF

Upload a PDF containing study material and QuizForge AI extracts the text before generating questions.

## Difficulty Modes

### Easy

Focuses on fundamental concepts, definitions, and basic understanding.

### Medium

Focuses on conceptual understanding, relationships, and moderate application.

### Hard

Focuses on deeper reasoning, advanced application, and challenging concepts.

### Adaptive

The difficulty changes dynamically according to the learner's performance.

For example:

```text
Correct Answer
    ↓
Increase Difficulty

Incorrect Answer
    ↓
Reduce or Maintain Difficulty
```

This allows the quiz to respond to the learner instead of keeping every question at the same difficulty.

## Question Types

### Mixed

Generates a balanced combination of different question types.

### Concept Based

Tests definitions, principles, theories, and fundamental understanding.

### Application Based

Tests the ability to apply knowledge to practical situations.

### Scenario Based

Presents realistic situations and asks the learner to identify the appropriate solution or concept.

### Code Based

Generates programming-related questions when the selected learning material contains relevant programming concepts.

## Practice Mode

Practice Mode is designed for learning.

After answering a question, the learner can receive:

* Correct or incorrect feedback
* Correct answer
* Explanation
* Progress information

This allows learners to understand mistakes while continuing through the quiz.

## Exam Mode

Exam Mode provides a test-style experience.

The learner can answer the generated questions and review the final performance after completing the quiz.

## Adaptive Learning

QuizForge AI uses the learner's responses to understand performance during the quiz.

The system can consider factors such as:

* Correct answers
* Incorrect answers
* Current difficulty
* Question performance
* Weak concepts

Based on the performance, the next question can be adjusted to provide a more personalized learning experience.

## Weak Area Detection

After completing a quiz, QuizForge AI analyzes the learner's performance and identifies areas that may require additional practice.

The result can include:

* Overall score
* Accuracy
* Strong areas
* Areas needing attention
* Learning recommendations
* Weak-area practice

The learner can use the weak-area practice option to focus on topics where improvement is needed.

## Question Repetition Prevention

QuizForge AI maintains a question history to reduce repeated questions when generating quizzes from the same learning source.

Previously used questions are considered during future generation requests so that the system can produce more varied practice.

A source identifier is also used to distinguish between different learning materials.

## Technology Stack

### Frontend

* Streamlit

### Programming Language

* Python

### Generative AI

* Groq API
* OpenAI GPT-OSS-120B model

### PDF Processing

* PyPDF2

### Environment Configuration

* python-dotenv

### Data Processing

* Python JSON processing
* Hash-based source identification
* In-memory quiz and question history management

## Requirements

* Python 3.10 or higher
* Groq API key
* Internet connection
* Required Python packages

## API Key Setup

Create a `.env` file in the project root directory.

```

## Using QuizForge AI

### Step 1: Choose the Learning Source

You can provide:

* A topic
* Study material
* A PDF

### Step 2: Select the Number of Questions

Available options:

* 5
* 10
* 15
* 20
* 30
* 40
* 50

### Step 3: Choose the Difficulty

Available options:

* Easy
* Medium
* Hard
* Adaptive

### Step 4: Choose the Question Type

Available options:

* Mixed
* Concept Based
* Application Based
* Scenario Based
* Code Based

### Step 5: Select the Learning Mode

Available modes:

* Practice Mode
* Exam Mode

### Step 6: Start the Quiz

Start the quiz and answer each question.

### Step 7: Review the Results

Review the score, accuracy, explanations, and AI-generated learning analysis.

### Step 8: Practice Weak Areas

Use the weak-area practice option to focus on topics where improvement is needed.

## Example Use Case

A student preparing for an examination can upload a PDF containing study material.

QuizForge AI can then:

```text
PDF
↓
Extract Study Material
↓
Analyze Content
↓
Generate Questions
↓
Student Answers
↓
Evaluate Performance
↓
Identify Weak Areas
↓
Recommend Further Practice
```

This turns static study material into an interactive learning experience.

## Application Link

https://quizforge-ai-xyf98uufuyqthzckjebjob.streamlit.app/

## Future Enhancements

Possible future improvements include:

* User accounts and personalized learning profiles
* Persistent learner progress
* Question bookmarking
* Quiz history dashboard
* Subject-wise performance tracking
* More advanced learning analytics
* Timed examinations
* Leaderboards for classroom environments
* Export quiz results
* Multiple-choice question banks
* Teacher-created quizzes
* Classroom quiz sharing
* Additional document formats
* Voice-based quiz interaction
* Multilingual quiz generation

## Project Vision

QuizForge AI aims to make learning more interactive by transforming ordinary educational content into an intelligent and adaptive assessment experience.

The goal is not only to generate questions, but to create a learning cycle where the system can:

```text
Learn from the Material
        ↓
Generate Questions
        ↓
Understand the Learner's Performance
        ↓
Identify Learning Gaps
        ↓
Adapt the Experience
        ↓
Support Better Practice
```

QuizForge AI brings together generative AI, adaptive learning, performance analysis, and interactive assessment to create a personalized learning experience from everyday study material.

```
```
