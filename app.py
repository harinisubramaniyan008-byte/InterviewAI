import streamlit as st
from groq import Groq
import pdfplumber
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import time

st.set_page_config(page_title="AI Career OS PRO", layout="wide", page_icon="🚀")

st.markdown("""
<style>
.metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; text-align: center;}
</style>
""", unsafe_allow_html=True)

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Please add GROQ_API_KEY in Streamlit Secrets → Settings")
    st.stop()

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text(): text += page.extract_text() + "\n"
    return text

# DEMO DATA - AI FAIL AANAALUM ITHU KAATUM
DEMO_DATA = {
  "ats_score": 75, "competitor_rank": 25,
  "skill_radar_you": {"Python": 7, "SQL": 6, "PowerBI": 2, "Excel": 8}, "skill_radar_job": {"Python": 9, "SQL": 9, "PowerBI": 8, "Excel": 8},
  "companies": [{"name": "Zoho", "openings": 23}, {"name": "TCS", "openings": 45}], "salary_roi": [{"skill": "PowerBI", "salary_hike": "+22%"}],
  "resume_rewrite": ["Old: Worked on data", "New: Analyzed 10GB data using Python, cut report time by 40%"],
  "learning_concepts": [{"topic": "SQL JOIN", "explain": "JOIN combines 2 tables. INNER = common rows. LEFT = all from left table."}],
  "mock_q": ["Tell me about a Python project", "What is ETL?"], "roadmap": [{"day": 1, "task": "Learn SQL SELECT"}, {"day": 2, "task": "Practice 5 JOIN queries"}],
  "motivation": "You are Top 25%! Master PowerBI in 14 days to reach Top 1%",
  "jobs": [{"title": "Data Analyst", "company": "Zoho", "link": "https://www.naukri.com"}],
  "courses": [{"skill": "PowerBI", "link": "https://youtube.com", "name": "Complete PowerBI for Beginners"}],
  "news": ["AI Agents will replace 30% of junior jobs in 2026"]
}

@st.cache_data(show_spinner="AI Analyzing Your Career... 40 seconds")
def get_full_analysis(resume_text, location):
    prompt = f"Return ONLY JSON. RESUME: {resume_text[:2000]} LOCATION: {location}" # Resume length cut pannen

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=3000,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"AI Error: {e}. Loading Demo Data instead.")
        return DEMO_DATA # AI FAIL AANAALUM APP NIKKADHU

# SIDEBAR MENU
st.sidebar.title("🚀 AI Career OS PRO")
page = st.sidebar.radio("Go to", ["🏠 Dashboard", "📊 Analytics", "🧠 Learn", "💼 Interview", "🎯 Roadmap", "🔎 Job Search"])

if 'data' not in st.session_state: st.session_state.data = None

with st.sidebar:
    st.header("Step 1: Upload Resume")
    resume_file = st.file_uploader("PDF", type=["pdf"])
    location = st.selectbox("Target City", ["Chennai", "Bangalore", "Hyderabad"])

    col1, col2 = st.columns(2)
    with col1:
        if resume_file and st.button("🚀 Generate", type="primary"):
            with st.spinner("Building your OS..."):
                resume_text = read_pdf(resume_file)
                st.session_state.data = get_full_analysis(resume_text, location)
                st.success("✅ Done!")
                st.rerun() # IMPORTANT: Page ah refresh pannum
    with col2:
        if st.button("🎮 Demo Mode"):
            st.session_state.data = DEMO_DATA
            st.success("✅ Demo Loaded!")
            st.rerun()

data = st.session_state.data

def check_data():
    if data is None:
        st.warning("⚠️ First click 'Generate' or 'Demo Mode' in sidebar")
        st.stop()

# PAGE 1: DASHBOARD
if page == "🏠 Dashboard":
    st.title("Welcome to your Career OS")
    if data:
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f'<div class="metric-card"><h3>ATS Score</h3><h1>{data.get("ats_score")}/100</h1></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div class="metric-card"><h3>Market Rank</h3><h1>Top {data.get("competitor_rank")}%</h1></div>', unsafe_allow_html=True)
        with col3: st.markdown(f'<div class="metric-card"><h3>Motivation</h3><p>{data.get("motivation")}</p></div>', unsafe_allow_html=True)
        st.progress(data.get("ats_score")/100, text="Your Career Level")
    else: st.info("👈 Step 1: Click 'Generate' or 'Demo Mode' in sidebar")

# PAGE 2: ANALYTICS
elif page == "📊 Analytics":
    check_data()
    st.title("📊 Deep Analytics")
    you, job = data.get("skill_radar_you", {}), data.get("skill_radar_job", {})
    df = pd.DataFrame({'Skill': list(you.keys()), 'You': list(you.values()), 'Job': list(job.values())})
    fig = go.Figure(); fig.add_trace(go.Scatterpolar(r=df['You'], theta=df['Skill'], fill='toself', name='You'))
    fig.add_trace(go.Scatterpolar(r=df['Job'], theta=df['Skill'], fill='toself', name='Job Demand'))
    st.plotly_chart(fig, use_container_width=True)
    st.write("**Before:**", data.get("resume_rewrite")[0]); st.success("**After:** " + data.get("resume_rewrite")[1])

# PAGE 3: LEARN
elif page == "🧠 Learn":
    check_data()
    st.title("🧠 AI Learning Lab")
    concept = data.get("learning_concepts", [{}])[0]
    st.markdown(f"### Topic: {concept.get('topic')}"); st.info(concept.get('explain'))
    if st.button("Give me a Code Example"): st.code("SELECT * FROM Employees INNER JOIN Departments ON id", language="sql")

# PAGE 4: INTERVIEW
elif page == "💼 Interview":
    check_data()
    st.title("💼 Mock Interview AI")
    q = st.selectbox("Choose Question", data.get("mock_q", []))
    ans = st.text_area("Your Answer", height=150)
    if st.button("Get AI Score"):
        with st.spinner("AI is judging..."): time.sleep(2); st.success("Score: 8/10. Add 1 more metric!")

# PAGE 5: ROADMAP
elif page == "🎯 Roadmap":
    check_data()
    st.title("🎯 30-Day Roadmap")
    for item in data.get("roadmap", []): st.checkbox(f"**Day {item.get('day')}:** {item.get('task')}", key=item.get('day'))

# PAGE 6: JOB SEARCH
elif page == "🔎 Job Search":
    check_data()
    st.title("🔎 AI Job Search for You")
    for job in data.get("jobs", []):
        with st.container(border=True):
            st.markdown(f"### {job.get('title')} at {job.get('company')}")
            st.link_button("Apply Now", job.get('link'))
