import streamlit as st
from groq import Groq
import pdfplumber
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import random

st.set_page_config(page_title="AI Career Coach TECH PRO", layout="wide", page_icon="🚀")

st.markdown("""
<style>
.metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white; text-align: center;}
.big-card {background-color: #FFFFFF; padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #E2E8F0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
.badge {background-color: #FFD700; color: black; padding: 5px 10px; border-radius: 20px; font-weight: bold; margin: 5px;}
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Career Coach TECH PRO")
st.caption("AI-Powered Career Intelligence + Learning Game | Built for 2026")

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

@st.cache_data(show_spinner="AI Analyzing... 30 seconds")
def get_pro_analysis(resume_text, location):
    prompt = f"""
    Return ONLY valid JSON with ALL these exact keys.
    RESUME: {resume_text}
    LOCATION: {location}

    {{
      "ats_score": 78,
      "ats_breakdown": {{"Keywords": 75, "Experience": 80, "Education": 90, "Skills": 70}},
      "skill_radar_you": {{"Python": 8, "SQL": 7, "PowerBI": 3, "ML": 4, "Excel": 9}},
      "skill_radar_job": {{"Python": 9, "SQL": 9, "PowerBI": 8, "ML": 7, "Excel": 8}},
      "companies": [{{"name": "Zoho", "openings": 23}}],
      "salary_roi": [{{"skill": "PowerBI", "salary_hike": "+22%"}}],
      "resume_rewrite": ["Old: Did work", "New: Improved process by 40%"],
      "competitor_rank": 23,
      "daily_skill": {{"title": "Prompt Engineering", "link": "youtube.com", "summary": "Learn to talk to AI in 1 min"}},
      "trending_jobs": ["AI Engineer", "Data Analyst", "Prompt Engineer"],
      "badges": ["ATS 70+ Unlocked", "Skill Hunter"]
    }}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=3000,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# SIDEBAR
with st.sidebar:
    st.header("Step 1: Upload Resume")
    resume_file = st.file_uploader("Upload PDF", type=["pdf"])
    location = st.selectbox("Target City", ["Chennai", "Bangalore", "Hyderabad"])

if resume_file:
    if st.button("🚀 Generate Tech Report", use_container_width=True, type="primary"):
        with st.spinner("AI is building your dashboard..."):
            resume_text = read_pdf(resume_file)
            try:
                data = get_pro_analysis(resume_text, location)
                st.session_state.data = data
                st.success("✅ Report Generated!")
            except Exception as e:
                st.error(f"AI JSON Error: {e}")

if 'data' in st.session_state:
    data = st.session_state.data

    ats = data.get("ats_score", 0)
    rank = data.get("competitor_rank", 0)
    companies = data.get("companies", [])

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f'<div class="metric-card"><h3>ATS Score</h3><h1>{ats}/100</h1></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="metric-card"><h3>Market Rank</h3><h1>Top {rank}%</h1></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="metric-card"><h3>Companies</h3><h1>{len(companies)} Hiring</h1></div>', unsafe_allow_html=True)

    # NEW TABS ADDED
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Skill Analytics", "🏢 Market Data", "✍️ AI Tools", "📈 Salary ROI", "🎮 Career Quest", "📺 Learn Hub"])

    with tab1: # OLD
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

    with tab2: # OLD
        st.subheader(f"Hiring Trend in {location}")
        if companies:
            df_comp = pd.DataFrame(companies)
            fig2 = px.bar(df_comp, x='name', y='openings', color='openings')
            st.plotly_chart(fig2, use_container_width=True)

    with tab3: # OLD
        st.subheader("AI Resume Bullet Rewriter")
        rewrite = data.get("resume_rewrite", ["N/A", "N/A"])
        st.write("**Before:**", rewrite[0])
        st.success("**After:** " + rewrite[1])

    with tab4: # OLD
        st.subheader("Skill = Money")
        roi = data.get("salary_roi", [])
        if roi: st.dataframe(pd.DataFrame(roi), use_container_width=True)

    with tab5: # NEW - GAME
        st.subheader("🎮 Your Career Quest")
        st.progress(ats/100, text=f"Level {ats//10} Career Warrior")
        st.write("**Unlock Badges:**")
        for badge in data.get("badges", []):
            st.markdown(f'<span class="badge">🏆 {badge}</span>', unsafe_allow_html=True)
        st.info("Complete 'Learn PowerBI' to get +22% Salary and +10 XP!")

    with tab6: # NEW - LEARNING
        st.subheader("📺 Today's 1-Minute Skill Byte")
        daily = data.get("daily_skill", {})
        st.markdown(f"### {daily.get('title', 'N/A')}")
        st.write(daily.get('summary', 'N/A'))
        st.link_button("Watch & Learn Now", daily.get('link', '#'))

        st.subheader("🔥 Trending Jobs in " + location)
        for job in data.get("trending_jobs", []):
            st.write(f"- 🚀 {job}")

else:
    st.info("👈 Step 1: Upload resume \n\n Step 2: Click 'Generate Tech Report'")
