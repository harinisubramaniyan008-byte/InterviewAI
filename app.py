import streamlit as st
from groq import Groq
import pdfplumber
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

st.set_page_config(page_title="AI Career OS PRO", layout="wide", page_icon="🚀", initial_sidebar_state="expanded")

# PRO UI
st.markdown("""
<style>
.metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white;}
.big-card {background-color: #1E293B; padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #334155;}
.stButton>button {background-color: #4F46E5; color: white; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.sidebar.error("⚠️ Add GROQ_API_KEY in Settings → Secrets")
    st.stop()

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text(): text += page.extract_text() + "\n"
    return text

def ask_ai(prompt):
    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], temperature=0.3, max_tokens=2000)
    return response.choices[0].message.content

# SESSION STATE
if 'data' not in st.session_state: st.session_state.data = None
if 'resume_text' not in st.session_state: st.session_state.resume_text = ""

# SIDEBAR
with st.sidebar:
    st.title("🚀 AI Career OS PRO v10.0")
    page = st.radio("Menu", ["🏠 Dashboard", "🧠 AI Doubt Clear", "💼 Live Mock Interview", "🔎 AI Job + Course Finder", "💻 Code Lab", "🎯 Project Generator", "📊 Skill Gap"])

    st.header("Step 1: Upload Resume")
    resume_file = st.file_uploader("PDF", type=["pdf"])
    if resume_file:
        st.session_state.resume_text = read_pdf(resume_file)
        st.success("✅ Resume Loaded")

data = st.session_state.data

# PAGE 1: DASHBOARD
if page == "🏠 Dashboard":
    st.title("AI Career Command Center")
    if st.session_state.resume_text == "":
        st.warning("👈 First upload your resume in sidebar")
    else:
        with st.spinner("AI is analyzing your resume..."):
            prompt = f"Analyze this resume and give JSON: ats_score, top_3_skills, top_3_gaps. RESUME: {st.session_state.resume_text[:3000]}"
            result = ask_ai(prompt)
            st.json(result) # REAL DATA

# PAGE 2: AI DOUBT CLEAR - REAL SEARCH
elif page == "🧠 AI Doubt Clear":
    st.title("🧠 Ask AI Anything Technical")
    st.write("Ex: 'Explain Docker in Tamil with example' or 'What is difference between INNER and LEFT JOIN'")
    doubt = st.text_area("Your Doubt")
    if st.button("Get Answer from AI"):
        with st.spinner("AI is thinking..."):
            ans = ask_ai(f"Explain this clearly with code example: {doubt}")
            st.markdown(ans)

# PAGE 3: LIVE MOCK INTERVIEW - REAL SCORING
elif page == "💼 Live Mock Interview":
    st.title("💼 AI Live Mock Interview")
    role = st.selectbox("Job Role", ["Data Analyst", "Python Developer", "Product Manager"])
    if st.button("Generate 5 Questions for Me"):
        with st.spinner("AI is creating questions from your resume..."):
            qs = ask_ai(f"Generate 5 interview questions for {role} based on this resume: {st.session_state.resume_text[:2000]}")
            st.session_state.qs = qs
            st.write(qs)

    ans = st.text_area("Type your answer here")
    if st.button("Get Real AI Feedback & Score"):
        with st.spinner("AI is judging your answer..."):
            feedback = ask_ai(f"Question: {qs}. My Answer: {ans}. Give score out of 10, feedback, and how to improve it.")
            st.success(feedback)

# PAGE 4: AI JOB + COURSE FINDER - LIVE
elif page == "🔎 AI Job + Course Finder":
    st.title("🔎 AI Job + Course Finder")
    search = st.text_input("What job do you want? Ex: 'Python Jobs in Chennai for freshers'")
    if st.button("Search with AI"):
        with st.spinner("AI is searching best jobs and courses..."):
            result = ask_ai(f"Find 5 real job openings and 3 best free youtube courses for: {search}. Give company, role, and link.")
            st.markdown(result)

# PAGE 5: CODE LAB
elif page == "💻 Code Lab":
    st.title("💻 Practice SQL + Python Here")
    lang = st.selectbox("Language", ["SQL", "Python"])
    code = st.text_area("Write your code here")
    if st.button("Run Code & Explain"):
        st.code(code, language=lang.lower())
        st.info("AI Explanation: " + ask_ai(f"Explain this {lang} code line by line: {code}"))

# PAGE 6: PROJECT GENERATOR
elif page == "🎯 Project Generator":
    st.title("🎯 AI Project Ideas for Your Resume")
    if st.button("Generate 3 Resume-Worthy Projects"):
        with st.spinner("AI is creating projects..."):
            projects = ask_ai(f"Generate 3 unique project ideas for a resume with these skills. Give project name, tech stack, and 3 bullet points: {st.session_state.resume_text[:2000]}")
            st.markdown(projects)

# PAGE 7: SKILL GAP
elif page == "📊 Skill Gap":
    st.title("📊 Your Skill Gap vs Market")
    job = st.text_input("Target Job: Ex: 'Data Scientist'")
    if st.button("Analyze Gap"):
        with st.spinner("AI is comparing..."):
            gap = ask_ai(f"Compare skills in this resume vs skills needed for {job}. Give missing skills and 30 day plan: {st.session_state.resume_text[:2000]}")
            st.markdown(gap)
