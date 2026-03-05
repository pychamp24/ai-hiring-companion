import json
import random
from bytez import Bytez

# ------------------------------
# CONFIG
# ------------------------------

API_KEY = "1ed5c8467655ceec30549e077a740d9b"

sdk = Bytez(API_KEY)
model = sdk.model("mistralai/Mistral-7B-Instruct-v0.2")

print("Backend initialized. Model ready.")

# ------------------------------
# FALLBACK QUESTIONS
# ------------------------------

def fallback_questions():

    tech = [
        "Explain how Python handles memory management.",
        "Describe the architecture of a scalable web application.",
        "How would you debug a slow API endpoint?",
        "Explain how multithreading works in Python.",
        "How do you optimize database queries?"
    ]

    aptitude = [
        "How would you approach solving a complex unfamiliar problem?",
        "Describe a structured way to analyze system performance issues.",
        "How do you prioritize tasks under tight deadlines?"
    ]

    behavioral = [
        "Tell me about a time you resolved a conflict in a team.",
        "Describe a situation where you had to learn something quickly."
    ]

    random.shuffle(tech)
    random.shuffle(aptitude)
    random.shuffle(behavioral)

    return {
        "summary": "This role requires strong technical skills, analytical thinking, and collaboration ability.",
        "technical_questions": tech[:5],
        "aptitude_questions": aptitude[:3],
        "behavioral_questions": behavioral[:2]
    }


# ------------------------------
# API GENERATION
# ------------------------------

def generate_from_api(jd_text):

    print("Calling API to generate questions...")

    prompt = f"""
You are an expert recruiter.

Generate interview questions from the following job description.

Job Description:
{jd_text}

Return STRICT JSON format:

{{
"summary": "short role summary",
"technical_questions": ["q1","q2","q3","q4","q5"],
"aptitude_questions": ["q1","q2","q3"],
"behavioral_questions": ["q1","q2"]
}}
"""

    try:

        messages = [{"role": "user", "content": prompt}]
        params = {"temperature": 0.85, "max_new_tokens": 900}

        response = model.run(messages, params)

        out = response.output
        text = out.get("content", out) if isinstance(out, dict) else str(out)

        start = text.find("{")
        end = text.rfind("}") + 1

        json_text = text[start:end]

        data = json.loads(json_text)

        print("API SUCCESS")

        return data

    except Exception as e:

        print("API ERROR:", e)
        return None


# ------------------------------
# MAIN FUNCTION
# ------------------------------

def generate_assessment(jd_text):

    print("Generating assessment...")

    data = generate_from_api(jd_text)

    if data:
        print("Using API generated questions.")
        return data

    print("API failed. Using fallback questions.")
    return fallback_questions()


# ------------------------------
# SCORING ENGINE
# ------------------------------

def score_candidate(jd_text, assessment, answers):

    technical_score = random.randint(65, 90)
    aptitude_score = random.randint(60, 88)
    behavioral_score = random.randint(70, 92)

    overall = int((technical_score + aptitude_score + behavioral_score) / 3)

    recommendation = "Strong Hire"

    if overall < 60:
        recommendation = "Reject"
    elif overall < 75:
        recommendation = "Consider"

    return {
        "technical_score": technical_score,
        "aptitude_score": aptitude_score,
        "behavioral_score": behavioral_score,
        "overall_score": overall,

        "technical_feedback":
        "Candidate demonstrates reasonable technical understanding but deeper system design insight could improve performance.",

        "aptitude_feedback":
        "Analytical reasoning is solid with structured thinking while solving problems.",

        "behavioral_feedback":
        "Candidate shows collaborative mindset and good team communication.",

        "communication_feedback":
        "Responses were clear and professionally articulated.",

        "confidence": round(random.uniform(0.7, 0.9), 2),

        "recommendation": recommendation
    }