import streamlit as st
from backend import generate_assessment

st.set_page_config(layout="wide")

# Role protection: only Recruiter can access
if st.session_state.get("role") != "Recruiter":
    st.warning("This page is restricted to this role.")
    st.stop()

st.title("Assessment Generator")
st.caption("Generate structured interview assessments from a job description")

# ---------------------------------------------------
# JD Input
# ---------------------------------------------------

jd_text = st.text_area(
    "Paste Job Description",
    height=250,
    key="jd_input"
)

if st.button("Generate Assessment"):

    if not jd_text.strip():
        st.warning("Please paste a job description.")
        st.stop()

    with st.spinner("Generating assessment..."):

        data = generate_assessment(jd_text)

        # store globally
        st.session_state.assessment_data = data
        st.session_state.jd_text = jd_text


# ---------------------------------------------------
# Display Assessment
# ---------------------------------------------------

assessment = st.session_state.get("assessment_data")

if assessment:

    st.divider()

    st.subheader("Role Summary")
    st.write(assessment.get("summary", "No summary generated"))

    st.divider()

    st.subheader("Generated Questions")

    tech = assessment.get("technical_questions", [])
    apt = assessment.get("aptitude_questions", [])
    beh = assessment.get("behavioral_questions", [])

    if not tech and not apt and not beh:
        st.warning("No questions generated.")
    else:

        if tech:
            st.markdown("### Technical Questions")
            for i, q in enumerate(tech, 1):
                st.write(f"{i}. {q}")

        if apt:
            st.markdown("### Aptitude Questions")
            for i, q in enumerate(apt, 1):
                st.write(f"{i}. {q}")

        if beh:
            st.markdown("### Behavioral Questions")
            for i, q in enumerate(beh, 1):
                st.write(f"{i}. {q}")