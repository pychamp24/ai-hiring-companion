import requests
import json
import random
import re

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

API_KEY = "1ed5c8467655ceec30549e077a740d9b"

API_URL = "https://api.bytez.ai/v1/chat/completions"

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

print("Backend initialized.")

# ---------------------------------------------------
# FALLBACK QUESTIONS (used if API fails)
# ---------------------------------------------------

def fallback_questions():

    tech = [
        "Explain how Python manages memory and garbage collection.",
        "Describe the architecture of a scalable backend system.",
        "How would you debug a slow API endpoint in production?",
        "Explain the difference between multithreading and multiprocessing.",
        "How would you optimize database queries for large datasets?"
    ]

    aptitude = [
        "How would you approach solving a complex unfamiliar problem?",
        "Explain a structured framework you use to analyze system failures.",
        "How do you prioritize tasks when multiple deadlines collide?"
    ]

    behavioral = [
        "Tell me about a time you resolved a conflict in a team.",
        "Describe a situation where you had to learn something very quickly."
    ]

    random.shuffle(tech)
    random.shuffle(aptitude)
    random.shuffle(behavioral)

    return {
        "summary": "The role requires technical problem solving, analytical reasoning, and collaborative teamwork.",
        "technical_questions": tech[:5],
        "aptitude_questions": aptitude[:3],
        "behavioral_questions": behavioral[:2]
    }


# ---------------------------------------------------
# API GENERATION
# ---------------------------------------------------

def generate_from_api(jd_text):

    print("Calling Bytez API...")

    prompt = f"""
You are an expert technical recruiter.

From the job description below generate interview questions.

Return STRICT JSON in this format:

{{
"summary": "Short role summary",
"technical_questions": ["question1","question2","question3","question4","question5"],
"aptitude_questions": ["question1","question2","question3"],
"behavioral_questions": ["question1","question2"]
}}

Job Description:
{jd_text}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.85
    }

    try:

        response = requests.post(API_URL, headers=headers, json=payload)

        data = response.json()

        text = data["choices"][0]["message"]["content"]

        # Extract JSON safely
        start = text.find("{")
        end = text.rfind("}") + 1

        json_text = text[start:end]

        parsed = json.loads(json_text)

        print("API SUCCESS")

        return parsed

    except Exception as e:

        print("API ERROR:", e)

        return None


# ---------------------------------------------------
# MAIN ASSESSMENT GENERATOR
# ---------------------------------------------------

def generate_assessment(jd_text):

    print("Generating assessment...")

    data = generate_from_api(jd_text)

    if data:
        print("Using API generated questions.")
        return data

    print("API failed. Using fallback questions.")

    return fallback_questions()


# ---------------------------------------------------
# SCORING ENGINE
# ---------------------------------------------------

def score_candidate(jd_text, assessment, answers):

    technical_answers = " ".join(
        v for k, v in answers.items() if k.startswith("technical_")
    )

    aptitude_answers = " ".join(
        v for k, v in answers.items() if k.startswith("aptitude_")
    )

    behavioral_answers = " ".join(
        v for k, v in answers.items() if k.startswith("behavioral_")
    )

    all_answers = technical_answers + aptitude_answers + behavioral_answers

    # -------------------------
    # Keyword overlap
    # -------------------------

    def keyword_overlap(jd, ans):

        jd_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", jd.lower()))
        ans_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", ans.lower()))

        if not jd_words:
            return 0

        overlap = len(jd_words.intersection(ans_words))

        score = min((overlap / len(jd_words)) * 40, 40)

        return round(score, 2)

    # -------------------------
    # Depth score
    # -------------------------

    def depth_score(text):

        words = len(text.split())

        if words > 200:
            return 20
        elif words > 120:
            return 15
        elif words > 60:
            return 10
        else:
            return 5

    # -------------------------
    # Behavioral score
    # -------------------------

    def behavioral_score(text):

        indicators = ["situation", "task", "action", "result", "team", "challenge"]

        count = sum(1 for word in indicators if word in text.lower())

        return min(count * 3, 20)

    # -------------------------
    # Communication score
    # -------------------------

    def communication_score(text):

        sentences = re.split(r"[.!?]", text)

        sentence_count = len([s for s in sentences if s.strip()])

        word_count = len(text.split())

        if word_count == 0:
            return 0

        avg_length = word_count / max(sentence_count, 1)

        clarity = 10 if 10 < avg_length < 25 else 6

        punctuation = 5 if "." in text else 3

        structure = 5 if sentence_count > 3 else 2

        return min(clarity + punctuation + structure, 20)

    # -------------------------
    # Scores
    # -------------------------

    tech_score = keyword_overlap(jd_text, technical_answers) + depth_score(technical_answers)
    apt_score = depth_score(aptitude_answers)
    beh_score = behavioral_score(behavioral_answers)
    comm_score = communication_score(all_answers)

    tech_score = min(tech_score, 40)
    apt_score = min(apt_score, 20)
    beh_score = min(beh_score, 20)

    overall = round(
        (tech_score * 0.4) +
        (apt_score * 0.2) +
        (beh_score * 0.25) +
        (comm_score * 0.15),
        2
    )

    # -------------------------
    # Recommendation
    # -------------------------

    if overall >= 80:
        recommendation = "Strong Hire"
    elif overall >= 65:
        recommendation = "Consider"
    elif overall >= 50:
        recommendation = "Borderline"
    else:
        recommendation = "Do Not Recommend"

    confidence = round(min(overall / 100 + 0.5, 1.0), 2)

    return {
        "technical_score": round(tech_score, 2),
        "aptitude_score": round(apt_score, 2),
        "behavioral_score": round(beh_score, 2),
        "communication_score": round(comm_score, 2),
        "overall_score": overall,
        "confidence": confidence,
        "recommendation": recommendation,
        "technical_feedback": "Candidate demonstrates reasonable technical capability but deeper system thinking could improve answers.",
        "aptitude_feedback": "Analytical reasoning appears structured though more detailed explanation would strengthen responses.",
        "behavioral_feedback": "Candidate shows collaborative mindset and ownership in responses.",
        "communication_feedback": "Responses were generally clear though some answers could benefit from stronger structure."
    }
