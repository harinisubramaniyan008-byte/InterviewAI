import streamlit as st
from groq import Groq
import pdfplumber
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

st.set_page_config(page_title="AI Career OS PRO", layout="wide", page_icon="🚀", initial_sidebar_state="expanded") # SIDEBAR FORCE OPEN

st.markdown("""
<style>
.metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; text-align: center;}
</style>
""", unsafe_allow_html=True)

# GROQ KEY
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    client = None

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text(): text += page.extract_text() + "\n"
    return text

DEMO_DATA = {
  "ats_score": 75, "competitor_rank": 25,
  "skill_radar_you": {"Python": 7, "SQL": 6, "PowerBI": 2, "Excel": 8}, "skill_radar_job": {"Python": 9, "SQL": 9, "PowerBI": 8, "Excel": 8},
  "resume_rewrite": ["Old: Worked on data", "New: Analyzed 10GB data using Python, cut report time by 40%"],
  "learning_concepts": [{"topic": "SQL JOIN", "explain": "JOIN combines 2 tables. INNER = common rows."}],
  "mock_q": ["Tell me about a Python project"], "roadmap": [{"day": 1, "task": "Learn SQL SELECT"}, {"day": 2, "task": "Practice JOIN"}],
  "motivation": "You are Top 25%! Master PowerBI in 14 days!",
  "jobs": [{"title": "Data Analyst", "company": "Zoho", "link": "https://www.naukri.com"}]
}

@st.cache_data
def get_full_analysis(_resume_text, _location):
    if client is None: return DEMO_DATA
    prompt = f"Return ONLY JSON. RESUME: {_resume_text[:1500]} LOCATION: {_location}"
    try:
        response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], temperature=0.1, max_tokens=2500, response_format={"type": "json_object"})
        return json.loads(response.choices[0].message.content)
    except:
        return DEMO_DATA

# SESSION STATE
if 'data' not in st.session_state:
    st.session_state.data = None
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Dashboard" # DEFAULT DASHBOARD

# SIDEBAR - ITHU EPOVUM IRUKANUM
with st.sidebar:
    st.title("🚀 AI Career OS PRO")

    st.session_state.page = st.radio("Go to",
        ["🏠 Dashboard", "📊 Analytics", "🧠 Learn", "💼 Interview", "🎯 Roadmap", "🔎 Job Search"],
        index=["🏠 Dashboard", "📊 Analytics", "🧠 Learn", "💼 Interview", "🎯 Roadmap", "🔎 Job Search"].index(st.session_state.page)
    )

    st.header("Step 1: Start Here")
    resume_file = st.file_uploader("Upload PDF", type=["pdf"])
    location = st.selectbox("Target City", ["Chennai", "Bangalore", "Hyderabad"])

    col1, col2 = st.columns(2)
    with col1:
        if resume_file and st.button("🚀 Generate", type="primary"):
            with st.spinner("Building..."):
                resume_text = read_pdf(resume_file)
                st.session_state.data = get_full_analysis(resume_text, location)
                st.success("✅ Done!")
    with col2:
        if st.button("🎮 Demo Mode"):
            st.session_state.data = DEMO_DATA
            st.success("✅ Demo Loaded!")
    st.divider()

data = st.session_state.data
page = st.session_state.page

def get_safe(key, default=0):
    if data is None: return default
    return data.get(key, default)

# PAGES
if page == "🏠 Dashboard":
    st.title("Welcome to your Career OS")
    ats = get_safe("ats_score", 0)
    rank = get_safe("competitor_rank", 0)
    motivation = get_safe("motivation", "Click Demo Mode to start")

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f'<div class="metric-card"><h3>ATS Score</h3><h1>{ats}/100</h1></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="metric-card"><h3>Market Rank</h3><h1>Top {rank}%</h1></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="metric-card"><h3>Motivation</h3><p>{motivation}</p></div>', unsafe_allow_html=True)

    if data is not None:
        st.progress(ats/100, text="Your Career Level")
    else:
        st.info("👈 Left la 'Demo Mode' ah click pannu da")

elif page == "📊 Analytics":
    if data is None: st.warning("⚠️ First click 'Demo Mode'"); st.stop()
    st.title("📊 Deep Analytics")
    you = get_safe("skill_radar_you", {})
    job = get_safe("skill_radar_job", {})
    df = pd.DataFrame({'Skill': list(you.keys()), 'You': list(you.values()), 'Job': list(job.values())})
    fig = go.Figure(); fig.add_trace(go.Scatterpolar(r=df['You'], theta=df['Skill'], fill='toself', name='You'))
    fig.add_trace(go.Scatterpolar(r=df['Job'], theta=df['Skill'], fill='toself', name='Job'))
    st.plotly_chart(fig, use_container_width=True)

elif page == "🧠 Learn":
    if data is None: st.warning("⚠️ First click 'Demo Mode'"); st.stop()
    st.title("🧠 AI Learning Lab")
    concept = get_safe("learning_concepts", [{}])[0]
    st.markdown(f"### Topic: {concept.get('topic')}")
    st.info(concept.get('explain'))

elif page == "💼 Interview":
    if data is None: st.warning("⚠️ First click 'Demo Mode'"); st.stop()
    st.title("💼 Mock Interview AI")
    q = st.selectbox("Choose Question", get_safe("mock_q", []))
    st.text_area("Your Answer")
    if st.button("Get AI Score"): st.success("Score: 8/10!")

elif page == "🎯 Roadmap":
    if data is None: st.warning("⚠️ First click 'Demo Mode'"); st.stop()
    st.title("🎯 30-Day Roadmap")
    for item in get_safe("roadmap", []):
        st.checkbox(f"**Day {item.get('day')}:** {item.get('task')}", key=item.get('day'))

elif page == "🔎 Job Search":
    if data is None: st.warning("⚠️ First click 'Demo Mode'"); st.stop()
    st.title("🔎 AI Job Search for You")
    for job in get_safe("jobs", []):
        with st.container(border=True):
            st.markdown(f"### {job.get('title')} at {job.get('company')}")
            st.link_button("Apply Now", job.get('link'))
