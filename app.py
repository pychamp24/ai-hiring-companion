import streamlit as st

st.set_page_config(
    page_title="AI Hiring Companion",
    page_icon="💼",
    layout="wide"
)

# Hide default Streamlit sidebar navigation
st.markdown(
    """
    <style>
    
    /* Hide Streamlit default pages navigation */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* Remove extra spacing created by hidden nav */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# Role selection & navigation
# ---------------------------------------------------
if "role" not in st.session_state:
    st.session_state["role"] = "Recruiter"

role = st.sidebar.radio(
    "Select your role",
    ["Recruiter", "Candidate"],
    index=0 if st.session_state["role"] == "Recruiter" else 1,
)

st.session_state["role"] = role

st.sidebar.markdown("### Navigation")

if role == "Recruiter":
    st.sidebar.page_link(
        "pages/Assessment_Generator.py",
        label="🧠 Assessment Generator",
    )
    st.sidebar.page_link(
        "pages/Recruiter_Dashboard.py",
        label="📊 Recruiter Dashboard",
    )
elif role == "Candidate":
    st.sidebar.page_link(
        "pages/Candidate_Test.py",
        label="🧑‍💼 Candidate Test",
    )

st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #f4f7fb 0%, #e9eef6 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Main container spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Headers */
h1, h2, h3 {
    font-weight: 600;
    letter-spacing: -0.02em;
    color: #0f172a;
}

/* Cards */
[data-testid="stExpander"] {
    border-radius: 12px !important;
    border: 1px solid rgba(148,163,184,0.2) !important;
    background: white !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: white;
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid rgba(148,163,184,0.15);
    box-shadow: 0 4px 12px rgba(15,23,42,0.05);
}

/* Buttons */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    background: linear-gradient(135deg, #2563eb, #1e3a8a);
    color: white;
    border: none;
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(37,99,235,0.25);
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    border: 1px solid rgba(148,163,184,0.2);
}

/* Divider spacing */
hr {
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

</style>
""", unsafe_allow_html=True)

st.title("💼 AI Hiring Companion")
st.caption("End-to-end AI powered hiring workflow")

st.divider()

st.markdown("""
### 🚀 Product Overview

This system enables:

1. 📄 Generate structured hiring assessments from job descriptions  
2. 🧑‍💼 Conduct AI-evaluated candidate tests  
3. 📊 Rank candidates using standardized scoring  

Use the sidebar to navigate through the hiring workflow.
""")

st.success("Navigate using the sidebar →")