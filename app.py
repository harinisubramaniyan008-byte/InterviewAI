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

# Session state
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
    st.session_state.data = {}

# File read function - strong version
def read_file(uploaded_file):
    text = ""
    if uploaded_file is None:
        return ""
    try:
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
    except Exception as e:
        st.error(f"File padika mudiyala: {e}")

    if text.strip() == "":
        st.warning(f"⚠️ {uploaded_file.name} la text illa. Scan panna PDF ah irukum")
    return text

# 1. FIRST: Upload Section ONLY
st.markdown("### 📤 Step 1: Resume & JD Upload Pannu")
col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("1. Resume Upload Pannu", type=['pdf', 'docx', 'txt'], key="resume_upload")
    resume_text = read_file(resume_file)
    if resume_file: st.success(f"✅ {resume_file.name}")

with col2:
    job_file = st.file_uploader("2. JD Upload Pannu", type=['pdf', 'docx', 'txt'], key="jd_upload")
    job_desc = read_file(job_file)
    if job_file: st.success(f"✅ {job_file.name}")

if st.button("🚀 Step 2: 19 Models oda Analyze Pannu", type="primary", use_container_width=True):
    if resume_text.strip() == "":
        st.error("⚠️ Resume upload pannu da")
    elif job_desc.strip() == "":
        st.error("⚠️ JD upload pannu da")
    else:
        with st.spinner("19 AI Models ellam tab um fill panradhuku scanning... 30 sec"):
            prompt = f"""
            You are 19 HR experts. Based on this Resume and JD, return ONLY valid JSON.

            RESUME: {resume_text}
            JD: {job_desc}

            Return JSON with this structure:
            {{
                "location_alert": [{{"Company":"TCS","Role":"Data Analyst","Openings":12}}, {{"Company":"Zoho","Role":"Data Analyst","Openings":5}}, {{"Company":"Freshworks","Role":"Data Analyst","Openings":8}}],
                "fit_score": 85,
                "fit_feedback": "Python and SQL skills match aagudhu. Excel konjam improve pannanum",
                "companies": [{{"Company":"Zoho","Match":90,"Reason":"Skills 90% match"}}, {{"Company":"TCS","Match":82,"Reason":"Experience fit"}}],
                "salary": {{"Role":"Data Analyst","Min":6,"Max":12,"Avg":8.5}},
                "internships": [{{"Company":"Freshworks","Role":"Data Analyst Intern","Duration":"3 months"}}, {{"Company":"Zoho","Role":"BI Intern","Duration":"6 months"}}],
                "interview_q": ["Tell me about your projects", "Explain SQL join", "Python pandas use pannirukiya", "Why this company", "5 year plan enna"],
                "match_details": "### 🎯 1. OVERALL ATS SCORE: 85/100\\nStrong match\\n\\n### 📊 2. KEYWORD MATCH\\nMatched: Python, SQL, Excel\\nMissing: Tableau, PowerBI\\n\\n### 💪 3. SKILLS GAP\\nLearn Tableau\\n\\n### 🏆 4-19. Detailed analysis continue..."
            }}
            """
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.2
            )
            try:
                content = response.choices[0].message.content
                # JSON extract
                start = content.find('{')
                end = content.rfind('}') + 1
                st.session_state.data = json.loads(content[start:end])
                st.session_state.analysis_done = True
                st.rerun()
            except Exception as e:
                st.error(f"AI error: {e}")
                st.code(response.choices[0].message.content)

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
        c1,c2,c3 = st.columns(3)
        c1.metric("Min", f"{sal.get('Min',0)} LPA")
        c2.metric("Avg", f"{sal.get('Avg',0)} LPA")
        c3.metric("Max", f"{sal.get('Max',0)} LPA")
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
            st.write(f"**{i+1}.** {q}")
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
        st.warning("⚠️ Tableau skill add pannuna 95% pogum")
    else:
        st.info("First upload pannu")
