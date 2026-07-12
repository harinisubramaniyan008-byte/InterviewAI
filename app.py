import streamlit as st
from groq import Groq
import pdfplumber
import docx
import pandas as pd

st.set_page_config(page_title="AI Career Coach Pro V2", layout="wide")
st.title("🎯 AI Career Coach Pro V2")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📍 Overview", "🏢 Companies", "💰 Salary", "🎓 Internships", "❓ Interview", "📊 Match %", "🔔 Alerts"])

# GROQ API Key
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ GROQ_API_KEY missing in Secrets")
    st.stop()

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

with tab1:
    st.header("1. Location Smart Alert 📍")
    st.write("Chennai la 5 companies iruku")
    
    data = {
        'Company': ['TCS', 'Zoho', 'Freshworks', 'Infosys', 'Wipro'],
        'Role': ['Data Analyst']*5,
        'Openings': [12, 5, 8, 10, 7]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    
    st.header("2. Company Fit Score 🎯")
    st.progress(82)
    st.write("**Zoho ku unga fit: 82%** - Python skill match aagudhu. Excel konjam improve pannanum")
    
    st.markdown("---")
    st.subheader("Upload Resume & JD for Full 19 Model Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        resume_file = st.file_uploader("Resume Upload", type=['pdf', 'docx', 'txt'], key="resume_upload")
        resume_text_area = st.text_area("Illa na Paste Pannu", height=200, key="resume_paste")
        resume_text = read_file(resume_file) if resume_file else resume_text_area

    with col2:
        job_file = st.file_uploader("JD Upload", type=['pdf', 'docx', 'txt'], key="jd_upload")
        job_text_area = st.text_area("JD Paste Pannu", height=200, key="jd_paste")
        job_desc = read_file(job_file) if job_file else job_text_area
    
    if st.button("🚀 Run 19 Models Analysis", type="primary", use_container_width=True):
        if resume_text.strip() and job_desc.strip():
            with st.spinner("19 AI Models scanning..."):
                prompt = f"""You are 19 HR experts. Analyze Resume vs JD.

RESUME: {resume_text}
JOB: {job_desc}

Give 19 points: 1.ATS Score 2.Keywords 3.Skills Gap 4.Experience 5.Education 6.Projects 7.Formatting 8.Achievements 9.Role Align 10.Industry Fit 11.Interview Q 12.Salary 13.Linkedin 14.Cover Letter 15.30-60-90 16.Red Flags 17.Quick Wins 18.Competitor 19.Final Rec"""
                response = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=4000
                )
                st.success("✅ Analysis Complete")
                st.markdown(response.choices[0].message.content)
        else:
            st.warning("Resume and JD rendu um podu")

with tab2:
    st.header("🏢 Companies")
    st.write("Company list varum - ipo sample data")

with tab3:
    st.header("💰 Salary")
    st.write("Salary benchmark varum")

with tab4:
    st.header("🎓 Internships")
    
with tab5:
    st.header("❓ Interview")
    
with tab6:
    st.header("📊 Match %")
    
with tab7:
    st.header("🔔 Alerts")
