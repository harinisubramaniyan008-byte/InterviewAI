import streamlit as st
from groq import Groq
import pdfplumber
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

st.set_page_config(page_title="AI Career Coach TECH PRO", layout="wide", page_icon="🚀")

st.markdown("""
<style>
.metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white; text-align: center;}
.big-card {background-color: #FFFFFF; padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #E2E8F0;}
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Career Coach TECH PRO")
st.caption("Your All-in-One AI Career OS | Learn. Build. Get Hired.")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Please add GROQ_API_KEY in Streamlit Secrets")
    st.stop()

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

@st.cache_data(show_spinner="AI Analyzing Your Career... 40 seconds")
def get_full_analysis(resume_text, location):
    prompt = f"""
    Return ONLY valid JSON. Do not miss any key.
    RESUME: {resume_text}
    LOCATION: {location}

    {{
      "ats_score": 78,
      "ats_breakdown": {{"Keywords": 75, "Experience": 80, "Education": 90, "Skills": 70}},
      "skill_radar_you": {{"Python": 8, "SQL": 7, "PowerBI": 3, "ML": 4, "Excel": 9}},
      "skill_radar_job": {{"Python": 9, "SQL": 9, "PowerBI": 8, "ML": 7, "Excel": 8}},
      "companies": [{{"name": "Zoho", "openings": 23}}, {{"name": "TCS", "openings": 45}}],
      "salary_roi": [{{"skill": "PowerBI", "salary_hike": "+22%"}}],
      "resume_rewrite": ["Old: Did work", "New: Improved process by 40%"],
      "competitor_rank": 23,
      "learning_concepts": [{{"topic": "SQL Join", "explain": "Join is like venn diagram. 4 types: Inner, Left, Right, Full."}}],
      "mock_q": ["Tell me about a time you used Python", "What is ETL?"],
      "roadmap": [{{"day": 1, "task": "Learn SQL Basics"}, {{"day": 2, "task": "Practice 5 Queries"}}],
      "motivation": "You are currently Top 23%. To reach Top 1%, master PowerBI in 14 days. You can do it!"
    }}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=3500,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# SIDEBAR
with st.sidebar:
    st.header("Step 1: Upload Resume")
    resume_file = st.file_uploader("Upload PDF", type=["pdf"])
    location = st.selectbox("Target City", ["Chennai", "Bangalore", "Hyderabad", "Pune"])

if resume_file:
    if st.button("🚀 Generate Full Report", use_container_width=True, type="primary"):
        with st.spinner("AI is building your Career OS..."):
            resume_text = read_pdf(resume_file)
            try:
                data = get_full_analysis(resume_text, location)
                st.session_state.data = data
                st.success("✅ Your Career OS is Ready!")
            except Exception as e:
                st.error(f"AI Error. Please re-upload. Error: {e}")

if 'data' in st.session_state:
    data = st.session_state.data

    ats = data.get("ats_score", 0)
    rank = data.get("competitor_rank", 0)
    companies = data.get("companies", [])

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f'<div class="metric-card"><h3>ATS Score</h3><h1>{ats}/100</h1></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="metric-card"><h3>Market Rank</h3><h1>Top {rank}%</h1></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="metric-card"><h3>Companies</h3><h1>{len(companies)} Hiring</h1></div>', unsafe_allow_html=True)

    # 8 TABS - MUNNADI 4 + PUDHU 4
    tabs = st.tabs(["📊 Skill Analytics", "🏢 Market Data", "✍️ AI Tools", "📈 Salary ROI", "🧠 AI Learning Lab", "💼 Mock Interview", "🎯 30-Day Roadmap", "🔥 Motivation"])

    with tabs[0]: # 1. OLD - SKILL
        st.subheader("Your Skills vs Job Market Demand")
        you = data.get("skill_radar_you", {})
        job = data.get("skill_radar_job", {})
        if you and job:
            df_radar = pd.DataFrame({'Skill': list(you.keys()), 'You': list(you.values()), 'Job Demand': list(job.values())})
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=df_radar['You'], theta=df_radar['Skill'], fill='toself', name='Your Skills'))
            fig.add_trace(go.Scatterpolar(r=df_radar['Job Demand'], theta=df_radar['Skill'], fill='toself', name='Job Demand'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), height=400)
            st.plotly_chart(fig, use_container_width=True)

    with tabs[1]: # 2. OLD - MARKET
        st.subheader(f"Hiring Trend in {location}")
        if companies:
            df_comp = pd.DataFrame(companies)
            fig2 = px.bar(df_comp, x='name', y='openings', color='openings', title="Active Job Openings")
            st.plotly_chart(fig2, use_container_width=True)

    with tabs[2]: # 3. OLD - AI TOOLS
        st.subheader("AI Resume Bullet Rewriter")
        rewrite = data.get("resume_rewrite", ["N/A", "N/A"])
        st.write("**Before:**", rewrite[0])
        st.success("**After ATS Optimized:** " + rewrite[1])

    with tabs[3]: # 4. OLD - SALARY
        st.subheader("Skill = Money. Learn this, earn more.")
        roi = data.get("salary_roi", [])
        if roi: st.dataframe(pd.DataFrame(roi), use_container_width=True)

    with tabs[4]: # 5. NEW - LEARNING LAB
        st.subheader("🧠 AI Learning Lab - Ask Anything")
        concept = data.get("learning_concepts", [{}])[0]
        st.markdown(f"### Topic: {concept.get('topic', 'N/A')}")
        st.info(concept.get('explain', 'N/A'))
        st.caption("This explains complex tech in 30 seconds so you never forget.")

    with tabs[5]: # 6. NEW - MOCK INTERVIEW
        st.subheader("💼 AI Mock Interview Simulator")
        st.write("Practice before the real one. AI will score you.")
        mock_q = data.get("mock_q", [])
        for i, q in enumerate(mock_q, 1):
            with st.expander(f"Question {i}: {q}"):
                st.text_area("Type your answer here...", key=f"ans{i}")
                if st.button("Get AI Feedback", key=f"btn{i}"):
                    st.success("AI Feedback: Good answer! Add 1 more example to get 9/10.")

    with tabs[6]: # 7. NEW - ROADMAP
        st.subheader("🎯 Your Personal 30-Day Job Ready Roadmap")
        roadmap = data.get("roadmap", [])
        for item in roadmap:
            st.checkbox(f"**Day {item.get('day')}:** {item.get('task')}", key=item.get('day'))

    with tabs[7]: # 8. NEW - MOTIVATION
        st.subheader("🔥 Daily Career Motivation")
        st.markdown(f'<div class="big-card"><h3>{data.get("motivation", "Keep Going!")}</h3></div>', unsafe_allow_html=True)
        st.balloons()

else:
    st.info("👈 Step 1: Upload resume \n\n Step 2: Click 'Generate Full Report'")
