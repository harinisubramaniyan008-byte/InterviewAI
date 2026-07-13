import streamlit as st
from groq import Groq
import pdfplumber
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

st.set_page_config(page_title="AI Career OS", layout="wide", page_icon="🚀")

# CSS for beauty
st.markdown("""
<style>
.metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; text-align: center;}
.big-card {background-color: #FFFFFF; padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #E2E8F0;}
.stButton>button {border-radius: 10px; height: 3em; width: 100%;}
</style>
""", unsafe_allow_html=True)

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Please add GROQ_API_KEY in Streamlit Secrets")
    st.stop()

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text(): text += page.extract_text() + "\n"
    return text

@st.cache_data(show_spinner="AI Analyzing Your Career... 40 seconds")
def get_full_analysis(resume_text, location):
    prompt = f"""
    Return ONLY valid JSON. RESUME: {resume_text} LOCATION: {location}
    {{
      "ats_score": 78, "competitor_rank": 23,
      "skill_radar_you": {{"Python": 8, "SQL": 7, "PowerBI": 3}}, "skill_radar_job": {{"Python": 9, "SQL": 9, "PowerBI": 8}},
      "companies": [{{"name": "Zoho", "openings": 23}}], "salary_roi": [{{"skill": "PowerBI", "salary_hike": "+22%"}}],
      "resume_rewrite": ["Old: Did work", "New: Improved by 40%"],
      "learning_concepts": [{{"topic": "SQL JOIN", "explain": "JOIN combines tables."}}],
      "mock_q": ["Tell me about Python project"], "roadmap": [{{"day": 1, "task": "Learn SQL"}}],
      "motivation": "You are Top 23%. Master PowerBI in 14 days!",
      "jobs": [{{"title": "Data Analyst", "company": "Zoho", "link": "naukri.com"}}],
      "courses": [{{"skill": "PowerBI", "link": "youtube.com", "name": "Complete PowerBI Course"}}],
      "news": ["AI agents are replacing 30% of jobs in 2026"]
    }}
    """
    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], temperature=0.2, max_tokens=4000, response_format={"type": "json_object"})
    return json.loads(response.choices[0].message.content)

# SIDEBAR MENU - ITHU DHAN MAGIC
st.sidebar.title("🚀 AI Career OS")
page = st.sidebar.radio("Go to",
    ["🏠 Dashboard", "📊 Analytics", "🧠 Learn", "💼 Interview", "🎯 Roadmap",
     "🔎 Job Search", "📚 Skill University", "📰 Tech News", "👥 Compare", "🎨 Portfolio", "❓ Ask AI"])

# SESSION STATE
if 'data' not in st.session_state: st.session_state.data = None

with st.sidebar:
    st.header("Upload Resume")
    resume_file = st.file_uploader("PDF", type=["pdf"])
    location = st.selectbox("Target City", ["Chennai", "Bangalore", "Hyderabad"])
    if resume_file and st.button("Generate Report", type="primary"):
        with st.spinner("Building your OS..."):
            resume_text = read_pdf(resume_file)
            st.session_state.data = get_full_analysis(resume_text, location)
            st.success("✅ Done!")

data = st.session_state.data

# PAGE 1: DASHBOARD
if page == "🏠 Dashboard":
    st.title("Welcome to your Career OS")
    if data:
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f'<div class="metric-card"><h3>ATS Score</h3><h1>{data.get("ats_score")}/100</h1></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div class="metric-card"><h3>Market Rank</h3><h1>Top {data.get("competitor_rank")}%</h1></div>', unsafe_allow_html=True)
        with col3: st.markdown(f'<div class="metric-card"><h3>Motivation</h3><p>{data.get("motivation")}</p></div>', unsafe_allow_html=True)
    else: st.info("👈 Upload resume to start")

# PAGE 2: ANALYTICS - MUNNADI 4 TAB IRUNDA IDHULA IRUKUM
elif page == "📊 Analytics":
    st.title("📊 Deep Analytics")
    if data:
        st.subheader("Your Skills vs Market")
        you, job = data.get("skill_radar_you", {}), data.get("skill_radar_job", {})
        if you:
            df = pd.DataFrame({'Skill': list(you.keys()), 'You': list(you.values()), 'Job': list(job.values())})
            fig = go.Figure(); fig.add_trace(go.Scatterpolar(r=df['You'], theta=df['Skill'], fill='toself')); fig.add_trace(go.Scatterpolar(r=df['Job'], theta=df['Skill'], fill='toself')); st.plotly_chart(fig)
        st.subheader("Salary ROI")
        st.dataframe(pd.DataFrame(data.get("salary_roi", [])))
        st.subheader("AI Resume Rewrite")
        st.write("Before:", data.get("resume_rewrite")[0]); st.success("After: " + data.get("resume_rewrite")[1])

# PAGE 3: LEARN
elif page == "🧠 Learn":
    st.title("🧠 AI Learning Lab")
    if data:
        concept = data.get("learning_concepts")[0]
        st.markdown(f"### {concept.get('topic')}"); st.info(concept.get('explain'))
        st.button("Explain with Example", help="Click to ask AI for code example")

# PAGE 4: INTERVIEW
elif page == "💼 Interview":
    st.title("💼 Mock Interview AI")
    if data:
        for i, q in enumerate(data.get("mock_q", [])):
            with st.expander(f"Q{i+1}: {q}"):
                st.text_area("Your Answer", key=i)
                st.button("Get Feedback", key=f"f{i}")

# PAGE 5: ROADMAP
elif page == "🎯 Roadmap":
    st.title("🎯 30-Day Roadmap")
    if data:
        for item in data.get("roadmap", []): st.checkbox(f"Day {item.get('day')}: {item.get('task')}", key=item.get('day'))

# PAGE 6: JOB SEARCH - NEW
elif page == "🔎 Job Search":
    st.title("🔎 AI Job Search for You")
    if data:
        st.write(f"Top jobs in {location} for you:")
        for job in data.get("jobs", []):
            with st.container(border=True):
                st.markdown(f"### {job.get('title')} at {job.get('company')}")
                st.link_button("Apply Now", job.get('link'))

# PAGE 7: SKILL UNIVERSITY - NEW
elif page == "📚 Skill University":
    st.title("📚 Learn Any Skill for Free")
    if data:
        for course in data.get("courses", []):
            st.markdown(f"**{course.get('skill')}**: [{course.get('name')}]({course.get('link')})")
        st.caption("All best courses in 1 place. No need to search on YouTube.")

# PAGE 8: TECH NEWS - NEW
elif page == "📰 Tech News":
    st.title("📰 What's Happening in Tech")
    if data:
        for news in data.get("news", []): st.info(f"🔥 {news}")

# PAGE 9: COMPARE - NEW
elif page == "👥 Compare":
    st.title("👥 How do you compare?")
    if data: st.metric("You are better than", f"{100 - data.get('competitor_rank')}% of candidates")

# PAGE 10: PORTFOLIO - NEW
elif page == "🎨 Portfolio":
    st.title("🎨 AI Portfolio Builder")
    st.write("Click below and AI will write your portfolio website code")
    if st.button("Generate My Portfolio"): st.code("<html><h1>My Projects</h1>...</html>", language="html")

# PAGE 11: ASK AI - NEW
elif page == "❓ Ask AI":
    st.title("❓ Ask AI Anything About Career")
    q = st.text_input("Ask: 'How to crack FAANG interview?'")
    if st.button("Ask"):
        with st.spinner("AI thinking..."): st.write("AI Answer: Practice DSA 2 hours daily...")
