import streamlit as st
import json
import random
import os
import hashlib
from groq import Groq
from dotenv import load_dotenv
from PyPDF2 import PdfReader
load_dotenv()
st.set_page_config(page_title='QuizForge AI', page_icon='⚡', layout='wide', initial_sidebar_state='expanded')
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    st.error('GROQ_API_KEY is missing. Add it to your .env file.')
    st.stop()
client = Groq(api_key=api_key)
MODEL = 'openai/gpt-oss-120b'
defaults = {'questions': [], 'current': 0, 'answers': [], 'score': 0, 'quiz_started': False, 'quiz_finished': False, 'weak_topics': [], 'source_text': '', 'topic_source': '', 'source_id': '', 'question_history': [], 'question_answered': False, 'last_selected': None, 'adaptive_difficulty': 'Medium', 'quiz_number': 1, 'active_source_type': 'Topic'}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value
st.markdown('\n<style>\n@import url(\'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap\');\n\nhtml, body, [class*="css"] {\n    font-family: \'DM Sans\', sans-serif;\n}\n.stApp {\n    background:\n        radial-gradient(circle at 5% 5%, rgba(34,197,94,0.10), transparent 25%),\n        radial-gradient(circle at 95% 10%, rgba(16,185,129,0.08), transparent 25%),\n        radial-gradient(circle at 50% 100%, rgba(134,239,172,0.10), transparent 30%),\n        #f7fbf8;\n    color: #17201a;\n}\n[data-testid="stHeader"] {\n    background: transparent;\n}\n[data-testid="stSidebar"] {\n    background: #ffffff;\n    border-right: 1px solid #dce9df;\n}\n[data-testid="stSidebar"] * {\n    color: #26352b;\n}\n.block-container {\n    max-width: 1240px;\n    padding-top: 2rem;\n    padding-bottom: 4rem;\n}\n.hero {\n    position: relative;\n    overflow: hidden;\n    padding: 48px;\n    border-radius: 32px;\n    background:\n        linear-gradient(135deg, #ffffff 0%, #f0fdf4 55%, #dcfce7 100%);\n    border: 1px solid #cce8d4;\n    box-shadow: 0 20px 60px rgba(22,101,52,0.10);\n    margin-bottom: 28px;\n}\n.hero:before {\n    content: "";\n    position: absolute;\n    width: 260px;\n    height: 260px;\n    right: -80px;\n    top: -100px;\n    border-radius: 50%;\n    background: rgba(34,197,94,0.12);\n    border: 1px solid rgba(34,197,94,0.12);\n}\n.hero:after {\n    content: "";\n    position: absolute;\n    width: 160px;\n    height: 160px;\n    right: 90px;\n    bottom: -90px;\n    border-radius: 50%;\n    background: rgba(134,239,172,0.18);\n}\n.hero-label {\n    display: inline-block;\n    padding: 7px 14px;\n    border-radius: 999px;\n    background: #dcfce7;\n    border: 1px solid #bbf7d0;\n    color: #15803d;\n    font-size: 11px;\n    font-weight: 800;\n    letter-spacing: 1.4px;\n}\n.hero h1 {\n    font-family: \'Space Grotesk\', sans-serif;\n    font-size: 60px;\n    line-height: 1;\n    margin: 20px 0 14px 0;\n    letter-spacing: -2.5px;\n    color: #102218;\n}\n.hero h1 span {\n    color: #16a34a;\n}\n.hero p {\n    max-width: 730px;\n    color: #506158;\n    font-size: 18px;\n    line-height: 1.7;\n}\n.status-pill {\n    position: absolute;\n    right: 35px;\n    top: 35px;\n    display: flex;\n    align-items: center;\n    gap: 8px;\n    padding: 9px 14px;\n    border-radius: 999px;\n    background: rgba(255,255,255,0.85);\n    border: 1px solid #cce8d4;\n    color: #15803d;\n    font-size: 12px;\n    font-weight: 700;\n}\n.status-dot {\n    width: 8px;\n    height: 8px;\n    border-radius: 50%;\n    background: #22c55e;\n    box-shadow: 0 0 12px rgba(34,197,94,0.65);\n}\n.section-title {\n    font-family: \'Space Grotesk\', sans-serif;\n    font-size: 28px;\n    font-weight: 700;\n    color: #17201a;\n    margin: 28px 0 8px 0;\n}\n.section-subtitle {\n    color: #718078;\n    font-size: 14px;\n    margin-bottom: 20px;\n}\n.feature-grid {\n    display: grid;\n    grid-template-columns: repeat(3, 1fr);\n    gap: 15px;\n    margin: 25px 0 32px 0;\n}\n.feature-card {\n    padding: 23px;\n    min-height: 130px;\n    border-radius: 22px;\n    background: rgba(255,255,255,0.90);\n    border: 1px solid #dce9df;\n    box-shadow: 0 10px 35px rgba(20,83,45,0.06);\n}\n.feature-icon {\n    width: 38px;\n    height: 38px;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    border-radius: 12px;\n    background: #dcfce7;\n    color: #15803d;\n    font-size: 17px;\n    margin-bottom: 13px;\n}\n.feature-card strong {\n    display: block;\n    color: #1c2b22;\n    font-size: 16px;\n    margin-bottom: 7px;\n}\n.feature-card span {\n    color: #718078;\n    font-size: 13px;\n    line-height: 1.5;\n}\n.workspace {\n    padding: 31px;\n    border-radius: 28px;\n    background: rgba(255,255,255,0.92);\n    border: 1px solid #dce9df;\n    box-shadow: 0 18px 55px rgba(20,83,45,0.07);\n    margin-bottom: 25px;\n}\n.source-intro {\n    padding: 18px 20px;\n    border-radius: 17px;\n    background: #f0fdf4;\n    border: 1px solid #d1fae5;\n    color: #456052;\n    margin-bottom: 20px;\n}\n.source-intro strong {\n    color: #166534;\n}\n.source-card {\n    padding: 21px;\n    border-radius: 19px;\n    background: #fbfefc;\n    border: 1px solid #dce9df;\n    margin-bottom: 16px;\n}\n.source-card h3 {\n    color: #1c2b22;\n    margin: 0 0 6px 0;\n}\n.source-card p {\n    color: #718078;\n    margin: 0;\n    font-size: 13px;\n}\n.question-card {\n    padding: 35px;\n    border-radius: 28px;\n    background: #ffffff;\n    border: 1px solid #cfe6d5;\n    box-shadow: 0 18px 55px rgba(20,83,45,0.09);\n    margin: 22px 0;\n}\n.question-meta {\n    display: flex;\n    gap: 8px;\n    flex-wrap: wrap;\n    margin-bottom: 14px;\n}\n.badge {\n    display: inline-block;\n    padding: 6px 11px;\n    border-radius: 999px;\n    background: #ecfdf3;\n    border: 1px solid #bbf7d0;\n    color: #15803d;\n    font-size: 11px;\n    font-weight: 800;\n}\n.question-number {\n    color: #16a34a;\n    font-size: 12px;\n    font-weight: 800;\n    letter-spacing: 1.2px;\n    text-transform: uppercase;\n}\n.question-card h2 {\n    font-family: \'Space Grotesk\', sans-serif;\n    font-size: 29px;\n    line-height: 1.42;\n    color: #18251d;\n    margin-top: 12px;\n}\n.stat-card {\n    padding: 20px;\n    border-radius: 19px;\n    background: #ffffff;\n    border: 1px solid #dce9df;\n    box-shadow: 0 8px 25px rgba(20,83,45,0.05);\n    text-align: center;\n}\n.stat-label {\n    color: #7b8981;\n    font-size: 11px;\n    text-transform: uppercase;\n    letter-spacing: 1px;\n    font-weight: 700;\n}\n.stat-value {\n    color: #17251b;\n    font-family: \'Space Grotesk\', sans-serif;\n    font-size: 29px;\n    font-weight: 700;\n    margin-top: 5px;\n}\n.result-card {\n    padding: 36px;\n    border-radius: 30px;\n    background:\n        radial-gradient(circle at 85% 20%, rgba(34,197,94,0.13), transparent 24%),\n        #ffffff;\n    border: 1px solid #cfe6d5;\n    box-shadow: 0 20px 65px rgba(20,83,45,0.09);\n}\n.score-number {\n    font-family: \'Space Grotesk\', sans-serif;\n    font-size: 70px;\n    font-weight: 800;\n    line-height: 1;\n    color: #16a34a;\n}\n.score-label {\n    color: #718078;\n    font-size: 13px;\n    margin-top: 8px;\n}\n.analysis-card {\n    padding: 23px;\n    border-radius: 21px;\n    background: #ffffff;\n    border: 1px solid #dce9df;\n    margin: 14px 0;\n    box-shadow: 0 8px 25px rgba(20,83,45,0.04);\n}\n.analysis-card h3 {\n    color: #1c2b22;\n    margin-bottom: 8px;\n}\n.analysis-card p {\n    color: #718078;\n    line-height: 1.6;\n}\n.insight-box {\n    padding: 20px;\n    border-radius: 18px;\n    background: #f0fdf4;\n    border: 1px solid #bbf7d0;\n    margin-top: 18px;\n}\n.insight-box strong {\n    color: #166534;\n}\n.footer {\n    text-align: center;\n    color: #839087;\n    font-size: 12px;\n    margin-top: 35px;\n}\ndiv.stButton > button {\n    border-radius: 13px;\n    border: 1px solid #16a34a;\n    background: linear-gradient(135deg, #16a34a, #22c55e);\n    color: white;\n    font-weight: 700;\n    min-height: 48px;\n    transition: all 0.2s ease;\n}\ndiv.stButton > button:hover {\n    border-color: #15803d;\n    transform: translateY(-1px);\n    box-shadow: 0 10px 28px rgba(22,163,74,0.22);\n}\n.stTextInput input,\n.stTextArea textarea {\n    background: #ffffff !important;\n    color: #1c2b22 !important;\n    border: 1px solid #cfe1d4 !important;\n    border-radius: 13px !important;\n}\n[data-baseweb="select"] > div {\n    background: #ffffff;\n    border-color: #cfe1d4;\n}\n.stProgress > div > div > div > div {\n    background: linear-gradient(90deg, #16a34a, #4ade80);\n}\n[data-testid="stRadio"] label {\n    color: #405047;\n}\n[data-testid="stFileUploader"] {\n    background: #f8fcf9;\n    border-radius: 16px;\n    padding: 8px;\n    border: 1px dashed #b9d8c1;\n}\n.stTabs [data-baseweb="tab-list"] {\n    gap: 8px;\n}\n.stTabs [data-baseweb="tab"] {\n    border-radius: 10px;\n    padding: 8px 16px;\n}\n@media (max-width: 800px) {\n    .hero {\n        padding: 30px;\n    }\n    .hero h1 {\n        font-size: 43px;\n    }\n    .status-pill {\n        position: static;\n        width: fit-content;\n        margin-top: 20px;\n    }\n    .feature-grid {\n        grid-template-columns: 1fr;\n    }\n    .question-card h2 {\n        font-size: 23px;\n    }\n}\n</style>\n', unsafe_allow_html=True)

def normalize_question(text):
    return ' '.join(str(text).lower().strip().split())

def create_source_id(source):
    return hashlib.sha256(source.strip().lower().encode('utf-8')).hexdigest()

def prepare_source(source):
    source = source.strip()
    if len(source) > 14000:
        source = source[:14000]
    return source

def get_history_for_prompt(limit=80):
    history = st.session_state.question_history[-limit:]
    if not history:
        return 'No previous questions have been used.'
    return '\n'.join((f'- {question}' for question in history))

def generate_questions(source, count, difficulty, question_type, extra_instruction=''):
    previous_questions = get_history_for_prompt()
    prompt = f"""\nYou are QuizForge AI, a universal educational assessment engine.\nYou can generate quizzes for ANY legitimate academic, educational,\nprofessional, creative, scientific, technical, medical, or general\nknowledge subject.\nThe system is NOT limited to computer science or artificial intelligence.\n\nIt can handle subjects such as:\nmathematics, physics, chemistry, biology, medicine, nursing, pharmacy,\nenvironmental science, computer science, artificial intelligence,\nengineering, commerce, economics, accounting, management, history,\ngeography, political science, sociology, psychology, languages,\nliterature, law, fashion designing, fine arts, education, school\nsubjects, college subjects, competitive examinations, professional\nlearning, and many other domains.\nDetermine the actual subject from the user's input.\n\nSOURCE MATERIAL OR TOPIC:\n{source}\nREQUESTED DIFFICULTY:\n{difficulty}\nREQUESTED QUESTION STYLE:\n{question_type}\nPREVIOUSLY USED QUESTIONS:\n{previous_questions}\nADDITIONAL INSTRUCTION:\n{extra_instruction}\nCreate exactly {count} NEW multiple-choice questions.\nRequirements:\n1. Create exactly {count} questions.\n2. Every question must have exactly four options.\n3. Only one option must be correct.\n4. The answer must exactly match one option.\n5. Questions must be appropriate for the actual subject.\n6. If detailed study material is provided, base questions primarily on that material.\n7. If only a topic is provided, use established knowledge about that topic.\n8. Never assume the topic is computer science or artificial intelligence.\n9. Do not repeat previous questions.\n10. Do not rephrase previous questions.\n11. Do not test the same knowledge point repeatedly.\n12. Vary the question structures.\n13. Make incorrect options plausible and relevant.\n14. Include a concise explanation.\n15. Include the main concept.\n16. Include the difficulty.\n17. If Adaptive is requested, assign appropriate difficulty levels.\n18. If Mixed is requested, vary suitable question styles.\n19. Application questions must actually require applying knowledge.\n20. Scenario questions must fit the selected subject.\n21. Code Based questions must only be used when the subject genuinely involves programming or code.\n22. Medical questions should remain educational and use established knowledge.\n23. Mathematical and scientific questions must be internally accurate.\n24. Do not invent information from supplied study material.\n25. Return valid JSON only.\nReturn exactly:\n{{\n    "questions": [\n        {{\n            "question": "Question text",\n            "options": [\n                "Option 1",\n                "Option 2",\n                "Option 3",\n                "Option 4"\n            ],\n            "answer": "The exact correct option text",\n            "explanation": "Short explanation",\n            "concept": "Main concept",\n            "difficulty": "Easy"\n        }}\n    ]\n}}\n"""
    response = client.chat.completions.create(model=MODEL, messages=[{'role': 'system', 'content': 'You are a universal educational quiz generator. Return only valid JSON.'}, {'role': 'user', 'content': prompt}], temperature=0.75, response_format={'type': 'json_object'})
    text = response.choices[0].message.content
    if not text:
        raise ValueError('The AI returned an empty response.')
    data = json.loads(text)
    if 'questions' not in data:
        raise ValueError('The AI response does not contain a questions field.')
    questions = data['questions']
    if not isinstance(questions, list):
        raise ValueError('The questions field is not a list.')
    valid_questions = []
    previous_history = {normalize_question(q) for q in st.session_state.question_history}
    current_batch = set()
    for question in questions:
        if not isinstance(question, dict):
            continue
        required_fields = ['question', 'options', 'answer', 'explanation', 'concept', 'difficulty']
        if not all((field in question for field in required_fields)):
            continue
        question_text = str(question['question']).strip()
        question_key = normalize_question(question_text)
        if not question_text:
            continue
        if question_key in previous_history:
            continue
        if question_key in current_batch:
            continue
        options = question['options']
        if not isinstance(options, list):
            continue
        if len(options) != 4:
            continue
        options = [str(option).strip() for option in options]
        if len(set(options)) != 4:
            continue
        answer = str(question['answer']).strip()
        if answer not in options:
            continue
        valid_questions.append({'question': question_text, 'options': options, 'answer': answer, 'explanation': str(question['explanation']).strip(), 'concept': str(question['concept']).strip(), 'difficulty': str(question['difficulty']).strip()})
        current_batch.add(question_key)
    if len(valid_questions) < count:
        raise ValueError(f'Only {len(valid_questions)} unique questions were generated out of {count} requested. Please generate the quiz again.')
    random.shuffle(valid_questions)
    selected_questions = valid_questions[:count]
    for question in selected_questions:
        st.session_state.question_history.append(question['question'])
    if len(st.session_state.question_history) > 150:
        st.session_state.question_history = st.session_state.question_history[-150:]
    return selected_questions

def generate_adaptive_question(source, difficulty, question_type):
    previous_questions = get_history_for_prompt()
    prompt = f'\nYou are QuizForge AI, a universal adaptive learning engine.\nGenerate ONE multiple-choice question for the subject or study material below.\nSUBJECT OR STUDY MATERIAL:\n{source}\n\nTARGET DIFFICULTY:\n{difficulty}\n\nQUESTION STYLE:\n{question_type}\n\nPREVIOUS QUESTIONS:\n{previous_questions}\nRequirements:\n1. Create exactly one question.\n2. Provide exactly four options.\n3. Only one option is correct.\n4. The answer must exactly match one option.\n5. Do not repeat or rephrase previous questions.\n6. Use terminology appropriate to the actual subject.\n7. Do not assume the subject is computer science or artificial intelligence.\n8. The question must genuinely match the requested difficulty.\n9. Include a concise explanation.\n10. Include the main concept.\n11. Set difficulty exactly to "{difficulty}".\n12. Return JSON only.\nReturn:\n{{\n    "question": "Question text",\n    "options": [\n        "Option 1",\n        "Option 2",\n        "Option 3",\n        "Option 4"\n    ],\n    "answer": "The exact correct option text",\n    "explanation": "Short explanation",\n    "concept": "Main concept",\n    "difficulty": "{difficulty}"\n}}\n'
    response = client.chat.completions.create(model=MODEL, messages=[{'role': 'system', 'content': 'You are a universal adaptive educational quiz generator. Return only valid JSON.'}, {'role': 'user', 'content': prompt}], temperature=0.85, response_format={'type': 'json_object'})
    text = response.choices[0].message.content
    if not text:
        raise ValueError('The AI returned an empty response.')
    question = json.loads(text)
    required_fields = ['question', 'options', 'answer', 'explanation', 'concept', 'difficulty']
    if not all((field in question for field in required_fields)):
        raise ValueError('The AI returned an incomplete question.')
    question_text = str(question['question']).strip()
    question_key = normalize_question(question_text)
    previous_history = {normalize_question(q) for q in st.session_state.question_history}
    if question_key in previous_history:
        raise ValueError('The AI generated a duplicate question.')
    options = question['options']
    if not isinstance(options, list):
        raise ValueError('The AI did not return a valid options list.')
    if len(options) != 4:
        raise ValueError('The AI did not return exactly four options.')
    options = [str(option).strip() for option in options]
    if len(set(options)) != 4:
        raise ValueError('The AI returned duplicate options.')
    answer = str(question['answer']).strip()
    if answer not in options:
        raise ValueError('The correct answer does not match an option.')
    result = {'question': question_text, 'options': options, 'answer': answer, 'explanation': str(question['explanation']).strip(), 'concept': str(question['concept']).strip(), 'difficulty': str(question['difficulty']).strip()}
    st.session_state.question_history.append(question_text)
    if len(st.session_state.question_history) > 150:
        st.session_state.question_history = st.session_state.question_history[-150:]
    return result

def extract_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + '\n'
    return text.strip()

def get_next_adaptive_difficulty(current_difficulty, was_correct):
    levels = ['Easy', 'Medium', 'Hard']
    if current_difficulty not in levels:
        current_difficulty = 'Medium'
    index = levels.index(current_difficulty)
    if was_correct:
        if index < 2:
            return levels[index + 1]
        return 'Hard'
    if index > 0:
        return levels[index - 1]
    return 'Easy'

def reset_quiz():
    st.session_state.questions = []
    st.session_state.current = 0
    st.session_state.answers = []
    st.session_state.score = 0
    st.session_state.quiz_started = False
    st.session_state.quiz_finished = False
    st.session_state.weak_topics = []
    st.session_state.question_answered = False
    st.session_state.last_selected = None
    st.session_state.adaptive_difficulty = 'Medium'

def reset_everything():
    reset_quiz()
    st.session_state.source_text = ''
    st.session_state.topic_source = ''
    st.session_state.source_id = ''
    st.session_state.question_history = []
    st.session_state.quiz_number = 1
    st.session_state.active_source_type = 'Topic'
st.markdown('\n<div class="hero">\n    <div class="status-pill">\n        <span class="status-dot"></span>\n        AI ENGINE READY\n    </div>\n    <div class="hero-label">UNIVERSAL AI LEARNING ENGINE</div>\n    <h1>Quiz<span>Forge</span> AI</h1>\n    <p>\n        Forge intelligent quizzes from any subject, topic, notes, or PDF.\n        Learn at your level, discover your weak areas, and turn knowledge\n        into mastery.\n    </p>\n</div>\n', unsafe_allow_html=True)
if not st.session_state.quiz_started:
    st.markdown('\n        <div class="feature-grid">\n            <div class="feature-card">\n                <div class="feature-icon">∞</div>\n                <strong>Any Subject</strong>\n                <span>From medicine and mathematics to fashion, science, arts, history and technology.</span>\n            </div>\n            <div class="feature-card">\n                <div class="feature-icon">↗</div>\n                <strong>Adaptive Learning</strong>\n                <span>Difficulty can respond to your performance as you move through the quiz.</span>\n            </div>\n            <div class="feature-card">\n                <div class="feature-icon">✦</div>\n                <strong>Fresh Questions</strong>\n                <span>QuizForge tracks used questions to reduce repetitive quizzes.</span>\n            </div>\n        </div>\n        ', unsafe_allow_html=True)
with st.sidebar:
    st.markdown('## QuizForge AI')
    st.caption('Universal AI Learning Engine')
    st.divider()
    st.markdown('### Build Your Quiz')
    question_count = st.selectbox('Number of Questions', [5, 10, 15, 20, 30, 40, 50], index=1)
    difficulty = st.selectbox('Difficulty', ['Easy', 'Medium', 'Hard', 'Adaptive'])
    question_type = st.selectbox('Question Style', ['Mixed', 'Concept Based', 'Application Based', 'Scenario Based', 'Code Based'])
    mode = st.radio('Learning Mode', ['Practice Mode', 'Exam Mode'])
    st.divider()
    st.markdown('### AI Engine')
    st.caption('Groq')
    st.caption('GPT-OSS 120B')
    st.divider()
    if st.button('Reset Everything', use_container_width=True):
        reset_everything()
        st.rerun()
if not st.session_state.quiz_started:
    st.markdown('<div class="section-title">Forge Your Quiz</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Give QuizForge anything you want to learn. The AI determines the appropriate subject and builds the experience around it.</div>', unsafe_allow_html=True)
    st.markdown('\n        <div class="source-intro">\n            <strong>One engine. Any subject.</strong>\n            &nbsp; Enter a topic, paste your own material, or upload a PDF.\n        </div>\n        ', unsafe_allow_html=True)
    source_tab1, source_tab2, source_tab3 = st.tabs(['◉ Topic', '◇ Study Material', '↑ PDF'])
    topic = ''
    study_material = ''
    with source_tab1:
        st.markdown('\n            <div class="source-card">\n                <h3>Explore Any Topic</h3>\n                <p>Enter a subject, chapter, concept, or topic.</p>\n            </div>\n            ', unsafe_allow_html=True)
        topic = st.text_input('Topic', placeholder='Organic Chemistry, Human Anatomy, Fashion Designing, Python, Indian History...')
    with source_tab2:
        st.markdown('\n            <div class="source-card">\n                <h3>Use Your Own Material</h3>\n                <p>Paste notes, textbook content, revision material, or class material.</p>\n            </div>\n            ', unsafe_allow_html=True)
        study_material = st.text_area('Study Material', placeholder='Paste your study material here...', height=220)
    with source_tab3:
        st.markdown('\n            <div class="source-card">\n                <h3>Transform a PDF</h3>\n                <p>Upload a readable PDF chapter, notes, textbook, or study document.</p>\n            </div>\n            ', unsafe_allow_html=True)
        uploaded_file = st.file_uploader('Upload PDF', type=['pdf'])
        if uploaded_file:
            try:
                pdf_text = extract_pdf(uploaded_file)
                if not pdf_text:
                    st.error('No readable text was found in this PDF.')
                else:
                    if len(pdf_text) > 14000:
                        pdf_text = pdf_text[:14000]
                    st.session_state.source_text = pdf_text
                    st.success(f'PDF ready — {len(pdf_text)} characters extracted.')
            except Exception as e:
                st.error('Unable to read the PDF.')
                st.exception(e)
    st.markdown('<div class="section-title">Ready to Forge?</div>', unsafe_allow_html=True)
    if st.button('⚡ FORGE MY QUIZ', type='primary', use_container_width=True):
        source = ''
        source_type = 'Topic'
        if topic.strip():
            source = topic.strip()
            source_type = 'Topic'
        elif study_material.strip():
            source = study_material.strip()
            source_type = 'Study Material'
        elif st.session_state.source_text:
            source = st.session_state.source_text
            source_type = 'PDF'
        else:
            st.warning('Enter a topic, paste study material, or upload a PDF.')
            st.stop()
        if len(source) < 5:
            st.warning('Please provide a more specific topic or more study material.')
            st.stop()
        source = prepare_source(source)
        new_source_id = create_source_id(source)
        if st.session_state.source_id and st.session_state.source_id != new_source_id:
            st.session_state.question_history = []
        st.session_state.source_id = new_source_id
        st.session_state.topic_source = source
        st.session_state.active_source_type = source_type
        st.session_state.quiz_number += 1
        st.session_state.adaptive_difficulty = 'Medium'
        with st.spinner('QuizForge is analyzing your material and forging the quiz...'):
            try:
                if difficulty == 'Adaptive':
                    first_question = generate_adaptive_question(source, 'Medium', question_type)
                    st.session_state.questions = [first_question]
                else:
                    st.session_state.questions = generate_questions(source, question_count, difficulty, question_type)
                st.session_state.current = 0
                st.session_state.answers = []
                st.session_state.score = 0
                st.session_state.quiz_started = True
                st.session_state.quiz_finished = False
                st.session_state.weak_topics = []
                st.session_state.question_answered = False
                st.session_state.last_selected = None
                st.rerun()
            except Exception as e:
                st.error('Quiz generation failed.')
                st.exception(e)
if st.session_state.quiz_started and (not st.session_state.quiz_finished):
    questions = st.session_state.questions
    current = st.session_state.current
    if difficulty == 'Adaptive':
        total = question_count
    else:
        total = len(questions)
    question = questions[current]
    progress = current / total
    st.progress(progress)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'\n            <div class="stat-card">\n                <div class="stat-label">Question</div>\n                <div class="stat-value">{current + 1}/{total}</div>\n            </div>\n            ', unsafe_allow_html=True)
    with col2:
        st.markdown(f'\n            <div class="stat-card">\n                <div class="stat-label">Score</div>\n                <div class="stat-value">{st.session_state.score}</div>\n            </div>\n            ', unsafe_allow_html=True)
    with col3:
        st.markdown(f"""\n            <div class="stat-card">\n                <div class="stat-label">Level</div>\n                <div class="stat-value">{question['difficulty']}</div>\n            </div>\n            """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""\n            <div class="stat-card">\n                <div class="stat-label">Mode</div>\n                <div class="stat-value">{mode.replace(' Mode', '')}</div>\n            </div>\n            """, unsafe_allow_html=True)
    st.markdown(f"""\n        <div class="question-card">\n            <div class="question-number">\n                QUESTION {current + 1}\n            </div>\n            <div class="question-meta">\n                <span class="badge">{question['difficulty']}</span>\n                <span class="badge">{question['concept']}</span>\n            </div>\n            <h2>{question['question']}</h2>\n        </div>\n        """, unsafe_allow_html=True)
    if not st.session_state.question_answered:
        selected = st.radio('Choose your answer', question['options'], key=f'question_{current}')
        if st.button('Submit Answer', type='primary', use_container_width=True):
            st.session_state.last_selected = selected
            correct = selected == question['answer']
            st.session_state.answers.append({'question': question['question'], 'selected': selected, 'correct': question['answer'], 'concept': question['concept'], 'difficulty': question['difficulty']})
            if correct:
                st.session_state.score += 1
            else:
                st.session_state.weak_topics.append(question['concept'])
            st.session_state.question_answered = True
            st.rerun()
    else:
        selected = st.session_state.last_selected
        was_correct = selected == question['answer']
        if was_correct:
            st.success('✓ Correct — knowledge point strengthened.')
        else:
            st.error(f"Not quite. Correct answer: {question['answer']}")
        if mode == 'Practice Mode':
            st.markdown(f"""\n                <div class="insight-box">\n                    <strong>AI Explanation</strong><br>\n                    {question['explanation']}\n                </div>\n                """, unsafe_allow_html=True)
        if current + 1 < total:
            if st.button('Continue →', type='primary', use_container_width=True):
                if difficulty == 'Adaptive':
                    next_difficulty = get_next_adaptive_difficulty(question['difficulty'], was_correct)
                    with st.spinner(f'Adapting your next question to {next_difficulty} level...'):
                        try:
                            next_question = generate_adaptive_question(st.session_state.topic_source, next_difficulty, question_type)
                            st.session_state.questions.append(next_question)
                            st.session_state.adaptive_difficulty = next_difficulty
                        except Exception as e:
                            st.error('Unable to generate the next adaptive question.')
                            st.exception(e)
                            st.stop()
                st.session_state.current += 1
                st.session_state.question_answered = False
                st.session_state.last_selected = None
                st.rerun()
        elif st.button('Finish Quiz', type='primary', use_container_width=True):
            st.session_state.quiz_finished = True
            st.rerun()
if st.session_state.quiz_finished:
    total = len(st.session_state.answers)
    score = st.session_state.score
    if total > 0:
        percentage = int(score / total * 100)
    else:
        percentage = 0
    if percentage >= 85:
        result_title = 'Excellent Mastery'
        result_message = 'Your performance shows a strong understanding of the material.'
    elif percentage >= 70:
        result_title = 'Strong Progress'
        result_message = 'You have a solid foundation. A little targeted practice can take you further.'
    elif percentage >= 50:
        result_title = 'Keep Building'
        result_message = 'You are making progress. Focus on the concepts highlighted below.'
    else:
        result_title = 'Practice Mode Recommended'
        result_message = 'Use the weak-area practice to strengthen your understanding step by step.'
    st.markdown(f"""\n        <div class="result-card">\n            <div class="hero-label">QUIZFORGE ANALYSIS COMPLETE</div>\n            <h1 style="font-family:'Space Grotesk',sans-serif;color:#17251b;margin-top:18px;">\n                {result_title}\n            </h1>\n            <div class="score-number">{percentage}%</div>\n            <div class="score-label">\n                {score} of {total} questions answered correctly\n            </div>\n            <div class="insight-box">\n                <strong>AI Learning Insight</strong><br>\n                {result_message}\n            </div>\n        </div>\n        """, unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your Performance</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'\n            <div class="stat-card">\n                <div class="stat-label">Correct Answers</div>\n                <div class="stat-value">{score}</div>\n            </div>\n            ', unsafe_allow_html=True)
    with col2:
        st.markdown(f'\n            <div class="stat-card">\n                <div class="stat-label">Accuracy</div>\n                <div class="stat-value">{percentage}%</div>\n            </div>\n            ', unsafe_allow_html=True)
    with col3:
        st.markdown(f'\n            <div class="stat-card">\n                <div class="stat-label">Questions</div>\n                <div class="stat-value">{total}</div>\n            </div>\n            ', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Learning Analysis</div>', unsafe_allow_html=True)
    weak = list(dict.fromkeys(st.session_state.weak_topics))
    if weak:
        st.markdown(f"""\n            <div class="analysis-card">\n                <h3>Areas to Improve</h3>\n                <p>{', '.join(weak)}</p>\n                <p>\n                    QuizForge identified these concepts from the questions\n                    you answered incorrectly. Targeted practice can focus\n                    on these areas next.\n                </p>\n            </div>\n            """, unsafe_allow_html=True)
    else:
        st.markdown('\n            <div class="analysis-card">\n                <h3>Strong Concept Coverage</h3>\n                <p>\n                    You did not miss any major concept during this quiz.\n                    Keep challenging yourself with higher-level questions.\n                </p>\n            </div>\n            ', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Question Review</div>', unsafe_allow_html=True)
    for i, answer in enumerate(st.session_state.answers):
        if answer['selected'] == answer['correct']:
            st.success(f"Q{i + 1}  ✓  Correct  ·  {answer['concept']}  ·  {answer['difficulty']}")
        else:
            st.error(f"Q{i + 1}  ×  Incorrect  ·  {answer['concept']}  ·  {answer['difficulty']}")
    st.markdown('<div class="section-title">Continue Learning</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button('↗ Practice Weak Areas', use_container_width=True):
            if weak:
                source = st.session_state.topic_source
                additional_instruction = f"\nFocus strongly on these concepts:\n{', '.join(weak)}\n\nCreate questions that help the learner understand,\napply, and distinguish these concepts.\n\nDo not repeat questions from the completed quiz.\n"
                with st.spinner('QuizForge is creating a targeted learning path...'):
                    try:
                        st.session_state.questions = generate_questions(source, 5, 'Adaptive', 'Application Based', additional_instruction)
                        st.session_state.current = 0
                        st.session_state.answers = []
                        st.session_state.score = 0
                        st.session_state.quiz_finished = False
                        st.session_state.quiz_started = True
                        st.session_state.question_answered = False
                        st.session_state.last_selected = None
                        st.session_state.weak_topics = []
                        st.session_state.adaptive_difficulty = 'Medium'
                        st.rerun()
                    except Exception as e:
                        st.error('Unable to generate targeted practice.')
                        st.exception(e)
            else:
                st.info('No weak areas were detected.')
    with col2:
        if st.button('⚡ Forge Another Quiz', use_container_width=True):
            reset_quiz()
            st.session_state.quiz_number += 1
            st.rerun()
st.markdown('\n    <div class="footer">\n        QuizForge AI · Forge Knowledge · Practice Smarter · Master Any Subject\n    </div>\n    ', unsafe_allow_html=True)