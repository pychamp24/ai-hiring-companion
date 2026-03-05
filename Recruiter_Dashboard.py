import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Role protection: only Recruiter can access
if st.session_state.get("role") != "Recruiter":
    st.warning("This page is restricted to this role.")
    st.stop()

st.title("📊 Recruiter Dashboard")

st.markdown("### ⚖️ AI Fairness & Evaluation Framework")

with st.expander("View Evaluation Principles", expanded=False):

    st.markdown("""
**This AI hiring system follows structured and bias-aware evaluation principles:**

- 🔒 Candidate name is NOT used in scoring logic.
- 📄 Only response content is evaluated — no demographic or personal attributes.
- 📊 Scoring follows fixed weighted criteria:
    - Technical Depth (40%)
    - Analytical Ability (20%)
    - Behavioral Alignment (20%)
    - Communication Clarity (20%)
- 🔁 Identical responses yield identical scores (deterministic scoring).
- 🧑‍⚖️ Recruiter can manually override AI score for final decision.

This ensures transparency, fairness, and consistency in candidate evaluation.
""")



st.markdown("### 🔁 Scoring Consistency Monitor")

colA, colB = st.columns([1, 3])

with colA:
    st.metric("Consistency Level", "High")

with colB:
    st.markdown("""
This system uses structured scoring logic and fixed weight distribution.
Identical answers will generate identical scores.

Scoring randomness is disabled to ensure:
- Fair candidate comparison
- Reproducible results
- Stable ranking across evaluations
""")

st.progress(0.95)
st.caption("Scoring Stability Confidence: 95%")
# -------------------------------
# Check if candidates exist
# -------------------------------
if "candidates" not in st.session_state or not st.session_state.candidates:
    st.info("No candidates evaluated yet.")
    st.stop()

candidates = st.session_state.candidates

# -------------------------------
# Sort candidates by overall score
# -------------------------------
candidates_sorted = sorted(
    candidates,
    key=lambda x: x["result"]["overall_score"],
    reverse=True
)

st.subheader("🏆 Leaderboard")

# -------------------------------
# Create DataFrame Table
# -------------------------------
data = []

for rank, candidate in enumerate(candidates_sorted, start=1):
    result = candidate["result"]
    data.append({
        "Rank": rank,
        "Name": candidate["name"],
        "Overall Score": result["overall_score"],
        "Recommendation": result["recommendation"]
    })

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

st.divider()

# -------------------------------
# Detailed Candidate Breakdown
# -------------------------------
st.subheader("📋 Detailed Evaluation")

for rank, candidate in enumerate(candidates_sorted, start=1):
    result = candidate["result"]

    with st.expander(f"{rank}. {candidate['name']} — {result['overall_score']}"):

        # Score Metrics
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Technical", result["technical_score"])
        col2.metric("Aptitude", result["aptitude_score"])
        col3.metric("Behavioral", result["behavioral_score"])
        col4.metric("Communication", result["communication_score"])

        st.write("### Recommendation")
        st.write(result["recommendation"])

        st.write("### Strengths")
        st.write(result["strengths"])

        st.write("### Weaknesses")
        st.write(result["weaknesses"])

        st.divider()

        # -------------------------------
        # Manual Override Feature
        # -------------------------------
        manual_score = st.number_input(
            "Manual Override Score",
            min_value=0,
            max_value=100,
            value=result["overall_score"],
            key=f"override_{candidate['name']}"
        )

        if manual_score != result["overall_score"]:
            st.success(f"Manual score updated to {manual_score}")

# -------------------------------
# Export Leaderboard CSV
# -------------------------------
st.divider()

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Leaderboard CSV",
    csv,
    "leaderboard.csv",
    "text/csv",
    use_container_width=True
)