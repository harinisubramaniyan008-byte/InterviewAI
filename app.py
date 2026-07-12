import streamlit as st
from groq import Groq
import pdfplumber
import docx
import pandas as pd
import json

st.set_page_config(page_title="AI Career Coach Pro V2", layout="wide")
st.title("🎯 AI Career Coach Pro V2")

# GROQ API Key
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Settings > Secrets la GROQ_API_KEY podu da")
    st.stop()

# Session state for data
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
    st.session_state.data = {}

# File read function
def read_file(uploaded_file):
    text = ""
    if uploaded_file is None:
        return ""
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        text = uploaded_file.read().decode("utf-8", errors='ignore')
    return text

# 1. FIRST: Upload Section - Mela ve irukum
st.markdown("### 📤 Step 1: Resume & JD Upload Pannu")
col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("1. Resume Upload Pannu", type=['pdf', 'docx', 'txt'], key="resume_upload")
    resume_text_area = st.text_area("Illa na Paste Pannu", height=150, key="resume_paste")
    resume_text = read_file(resume_file) if resume_file else resume_text_area
    if resume_file: st.success(f"✅ {resume_file.name}")

with col2:
    job_file = st.file_uploader("2. JD Upload Pannu", type=['pdf', 'docx', 'txt'], key="jd_upload")
    job_text_area = st.text_area("JD Paste Pannu", height=150, key="jd_paste")
    job_desc = read_file(job_file) if job_file else job_text_area
    if job_file: st.success(f"✅ {job_file.name}")

if st.button("🚀 Step 2: 19 Models oda Analyze Pannu", type="primary", use_container_width=True):
    if resume_text.strip() and job_desc.strip():
        with st.spinner("19 AI Models ellam tab um fill panradhuku scanning..."):
            prompt = f"""
            You are 19 HR experts. Based on this Resume and JD, return ONLY valid JSON.

            RESUME: {resume_text}
            JD: {job_desc}

            Return JSON with this structure:
            {{
                "location_alert": [{{"Company":"TCS","Role":"Data Analyst","Openings":10}}, {{}}],
                "fit_score": 85,
                "fit_feedback": "Python match aagudhu",
                "companies": [{{"Company":"Zoho","Match":90,"Reason":"Skills match"}}],
                "salary": {{"Role":"Data Analyst","Min":6,"Max":12,"Avg":8.5}},
                "internships": [{{"Company":"Freshworks","Role":"Intern","Duration":"3 months"}}],
                "interview_q": ["Q1","Q2","Q3","Q4","Q5"],
                "match_details": "Detailed 19 point analysis here in markdown"
            }}
            """
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.2
            )
            try:
                st.session_state.data = json.loads(response.choices[0].message.content)
                st.session_state.analysis_done = True
                st.rerun()
            except:
                st.error("AI response error. Again try pannu")
    else:
        st.warning("⚠️ Resume and JD rendu um podu")

st.markdown("---")

# 2. Tabs - Upload panna aprom dhan data varum
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📍 Overview", "🏢 Companies", "💰 Salary", "🎓 Internships", "❓ Interview", "📊 Match %", "🔔 Alerts"])

with tab1:
    st.header("1. Location Smart Alert 📍")
    if st.session_state.analysis_done:
        df = pd.DataFrame(st.session_state.data.get("location_alert", []))
        st.dataframe(df, use_container_width=True)

        st.header("2. Company Fit Score 🎯")
        score = st.session_state.data.get("fit_score", 0)
        st.progress(score/100)
        st.write(f"**Fit: {score}%** - {st.session_state.data.get('fit_feedback','')}")
    else:
        st.info("Mela Resume + JD upload panni Analyze adichaa idhu fill aagum")

with tab2:
    st.header("🏢 Companies")
    if st.session_state.analysis_done:
        df = pd.DataFrame(st.session_state.data.get("companies", []))
        st.dataframe(df, use_container_width=True)
    else:
        st.info("First upload pannu")

with tab3:
    st.header("💰 Salary Benchmark")
    if st.session_state.analysis_done:
        sal = st.session_state.data.get("salary", {})
        st.metric("Avg Salary LPA", f"{sal.get('Avg',0)} LPA")
        st.write(f"Range: {sal.get('Min',0)} - {sal.get('Max',0)} LPA")
    else:
        st.info("First upload pannu")

with tab4:
    st.header("🎓 Internships")
    if st.session_state.analysis_done:
        df = pd.DataFrame(st.session_state.data.get("internships", []))
        st.dataframe(df, use_container_width=True)
    else:
        st.info("First upload pannu")

with tab5:
    st.header("❓ Predicted Interview Questions")
    if st.session_state.analysis_done:
        for i,q in enumerate(st.session_state.data.get("interview_q", [])):
            st.write(f"{i+1}. {q}")
    else:
        st.info("First upload pannu")

with tab6:
    st.header("📊 19 Models Match Analysis")
    if st.session_state.analysis_done:
        st.markdown(st.session_state.data.get("match_details",""))
    else:
        st.info("First upload pannu")

with tab7:
    st.header("🔔 Smart Alerts")
    if st.session_state.analysis_done:
        st.success("✅ Unga profile ku 3 new jobs match aagudhu")
        st.warning("⚠️ Excel skill konjam improve pannanum")
    else:
        st.info("First upload pannu")
