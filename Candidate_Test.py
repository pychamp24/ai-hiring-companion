import streamlit as st
import time
from backend import score_candidate

st.set_page_config(layout="wide")

st.markdown("## 🧑‍💼 Candidate Assessment Portal")
st.caption("Structured, bias-aware AI evaluation workflow")

# ---------------------------------------------------
# Check if assessment exists
# ---------------------------------------------------

if "assessment_data" not in st.session_state or not st.session_state.assessment_data:
    st.warning("⚠ Please generate an assessment first.")
    st.stop()

if "candidates" not in st.session_state:
    st.session_state.candidates = []

assessment = st.session_state.assessment_data
jd_text = st.session_state.jd_text


# ---------------------------------------------------
# Candidate Info
# ---------------------------------------------------

st.subheader("Candidate Information")

candidate_name = st.text_input("Full Name")

st.divider()

answers = {}

# ---------------------------------------------------
# Progress Tracking
# ---------------------------------------------------

total_questions = (
    len(assessment.get("technical_questions", []))
    + len(assessment.get("aptitude_questions", []))
    + len(assessment.get("behavioral_questions", []))
)

answered_count = 0


# ---------------------------------------------------
# Technical Questions
# ---------------------------------------------------

st.subheader("🛠 Technical Questions")

for i, question in enumerate(assessment.get("technical_questions", [])):
    answers[f"technical_{i}"] = st.text_area(
        question,
        height=120,
        key=f"tech_{i}"
    )


# ---------------------------------------------------
# Aptitude Questions
# ---------------------------------------------------

st.subheader("🧠 Aptitude Questions")

for i, question in enumerate(assessment.get("aptitude_questions", [])):
    answers[f"aptitude_{i}"] = st.text_area(
        question,
        height=120,
        key=f"apt_{i}"
    )


# ---------------------------------------------------
# Behavioral Questions
# ---------------------------------------------------

st.subheader("🤝 Behavioral Questions")

for i, question in enumerate(assessment.get("behavioral_questions", [])):
    answers[f"behavioral_{i}"] = st.text_area(
        question,
        height=120,
        key=f"beh_{i}"
    )

st.divider()


# ---------------------------------------------------
# Progress Bar
# ---------------------------------------------------

answered_count = sum(1 for a in answers.values() if a.strip())

if total_questions > 0:
    progress_ratio = answered_count / total_questions
else:
    progress_ratio = 0

st.markdown("### 📈 Test Completion Progress")

st.progress(progress_ratio)

st.caption(f"{answered_count} of {total_questions} questions answered")


# ---------------------------------------------------
# Submit Test
# ---------------------------------------------------

if st.button("🚀 Submit Test", use_container_width=True):

    if not candidate_name.strip():
        st.warning("⚠ Please enter candidate name.")
        st.stop()

    if not any(answer.strip() for answer in answers.values()):
        st.warning("⚠ Please answer at least one question.")
        st.stop()

    with st.spinner("🔍 AI is analyzing responses..."):

        progress_bar = st.progress(0)

        for i in range(1, 101, 10):
            progress_bar.progress(i / 100)
            time.sleep(0.08)

        try:
            result = score_candidate(jd_text, assessment, answers)

        except Exception as e:
            st.error("Evaluation failed.")
            st.exception(e)
            st.stop()

    # ---------------------------------------------------
    # Save candidate result
    # ---------------------------------------------------

    st.session_state.candidates.append({
        "name": candidate_name,
        "result": result
    })

    st.success("✅ Evaluation Complete & Saved")


    # ---------------------------------------------------
    # Score Summary
    # ---------------------------------------------------

    st.subheader("📊 Candidate Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Technical", result.get("technical_score", 0))
    col2.metric("Aptitude", result.get("aptitude_score", 0))
    col3.metric("Behavioral", result.get("behavioral_score", 0))
    col4.metric("Overall", result.get("overall_score", 0))

    st.divider()


    # ---------------------------------------------------
    # AI Feedback Sections
    # ---------------------------------------------------

    st.subheader("🧠 AI Evaluation Explanation")

    with st.expander("Technical Feedback", expanded=True):
        st.write(result.get("technical_feedback"))

    with st.expander("Aptitude Feedback"):
        st.write(result.get("aptitude_feedback"))

    with st.expander("Behavioral Feedback"):
        st.write(result.get("behavioral_feedback"))

    with st.expander("Communication Feedback"):
        st.write(result.get("communication_feedback"))

    st.divider()


    # ---------------------------------------------------
    # Confidence Score
    # ---------------------------------------------------

    st.subheader("🤖 AI Confidence Level")

    confidence = result.get("confidence", 0.75)

    st.progress(confidence)

    st.caption(f"Confidence Score: {int(confidence * 100)}%")


    st.divider()


    # ---------------------------------------------------
    # Final Recommendation
    # ---------------------------------------------------

    st.subheader("📌 Final Recommendation")

    st.success(result.get("recommendation", "N/A"))

    st.divider()


    # ---------------------------------------------------
    # Navigation to dashboard
    # ---------------------------------------------------

    if st.button("➡ Go to Recruiter Dashboard"):
        st.switch_page("pages/3_📊_Recruiter_Dashboard.py")