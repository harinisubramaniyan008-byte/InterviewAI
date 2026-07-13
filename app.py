import streamlit as st
from groq import Groq
import pdfplumber
from docx import Document
import pandas as pd
import plotly.graph_objects as go
import json
import re

st.set_page_config(page_title="AI Career Coach Pro", layout="wide", page_icon="🚀")

# CSS for trending look
st.markdown("""
<style>
.big-card {background-color: #1E293B; padding: 20px; border-radius: 15px; margin-bottom: 20px;}
.metric-card {background-color: #0F172A; padding: 15px; border-radius: 10px; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Career Coach PRO Dashboard")
st.caption("Upload once. Get everything. Built for 2026.")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Please add GROQ_API_KEY in Streamlit Secrets")
    st.stop()

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

@st.cache_data
def get_ai_analysis(resume_text, location):
    prompt = f"""
    You are a Senior AI Career Coach. Return ONLY valid JSON. No extra text.

    RESUME: {resume_text}
    LOCATION: {location}

    Return JSON with these keys:
    "ats_score": int,
    "ats_breakdown": {{"Keywords": int, "Experience": int, "Education": int, "Skills": int}},
    "strengths": [3 points],
    "weaknesses": [3 points],
    "top_companies": [{{"name": "", "why": ""}} x 5],
    "missing_skills": [{{"skill": "", "course": ""}} x 5],
    "salary": [{{"role": "", "fresher": "", "mid": "", "senior": ""}} x 3],
    "interview_q": [5 questions],
    "job_match": [{{"title": "", "percent": int}} x 5]
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=3000,
        response_format={"type": "json_object"} # JSON la varanum
    )
    return json.loads(response.choices[0].message.content)

# SIDEBAR
with st.sidebar:
    st.header("1. Upload Resume")
    resume_file = st.file_uploader("PDF / DOCX", type=["pdf", "docx"])
    st.header("2. Target Location")
    location = st.selectbox("", ["Chennai", "Bangalore", "Hyderabad", "Pune", "Mumbai", "Remote"])

if resume_file and st.button("🚀 Generate Dashboard", use_container_width=True):
    with st.spinner("AI is building your dashboard..."):
        if resume_file.type == "application/pdf":
            resume_text = read_pdf(resume_file)
        else:
            resume_text = Document(resume_file)
            resume_text = "\n".join([para.text for para in resume_text.paragraphs])

        data = get_ai_analysis(resume_text, location)
        st.session_state.data = data

if 'data' in st.session_state:
    data = st.session_state.data

    # TABS - TRENDING UI
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🏢 Companies", "📈 Skills & Salary", "❓ Interview", "🎯 Actions"])

    with tab1: # OVERVIEW
        st.subheader("Instant ATS Score")
        col1, col2 = st.columns([1,2])
        with col1:
            st.metric("Overall Score", f"{data['ats_score']}/100")
        with col2:
            # Radar Chart
            fig = go.Figure(data=go.Scatterpolar(
                r=list(data['ats_breakdown'].values()),
                theta=list(data['ats_breakdown'].keys()),
                fill='toself'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="big-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.write("**✅ Strengths**"); [st.write(f"- {s}") for s in data['strengths']]
        with c2: st.write("**❌ Weaknesses**"); [st.write(f"- {w}") for w in data['weaknesses']]
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2: # COMPANIES
        st.subheader(f"Top 5 Companies Hiring in {location}")
        for comp in data['top_companies']:
            st.markdown(f'<div class="big-card"><h4>{comp["name"]}</h4><p>{comp["why"]}</p></div>', unsafe_allow_html=True)

    with tab3: # SKILLS
        st.subheader("Skill Gap & Learning Path")
        for skill in data['missing_skills']:
            st.info(f"**Missing: {skill['skill']}** → Learn here: {skill['course']}")

        st.subheader("Salary Benchmark in INR")
        df = pd.DataFrame(data['salary'])
        st.dataframe(df, use_container_width=True)

    with tab4: # INTERVIEW
        st.subheader("Top 5 Predicted Interview Questions")
        for i, q in enumerate(data['interview_q'], 1):
            st.write(f"{i}. {q}")

    with tab5: # JOB MATCH
        st.subheader("Best Job Matches For You")
        for job in data['job_match']:
            st.progress(job['percent']/100, text=f"{job['title']} - {job['percent']}% Match")

else:
    st.info("Upload your resume and click 'Generate Dashboard' to start")
