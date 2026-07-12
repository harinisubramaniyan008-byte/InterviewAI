import streamlit as st
from groq import Groq
import pdfplumber
import docx

st.set_page_config(page_title="AI Career Coach Pro", layout="wide")
st.title("🎯 AI Career Coach Pro - 15 Models")

# 1. GROQ API Key
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ GROQ_API_KEY missing in Secrets")
    st.stop()

# 2. File padikka function
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
        text = uploaded_file.read().decode("utf-8")
    return text

# 3. Input Section
col1, col2 = st.columns(2)
with col1:
    st.subheader("📄 Resume")
    resume_file = st.file_uploader("Resume Upload Pannu", type=['pdf', 'docx', 'txt'], key="resume_upload")
    resume_text_area = st.text_area("Illa na inga Paste Pannu", height=250, key="resume_paste")
    resume_text = read_file(resume_file) if resume_file else resume_text_area
    if resume_file:
        st.success(f"✅ {resume_file.name} loaded")

with col2:
    st.subheader("💼 Job Description")
    job_file = st.file_uploader("JD Upload Pannu", type=['pdf', 'docx', 'txt'], key="jd_upload")
    job_text_area = st.text_area("JD ah inga Paste Pannu", height=250, key="jd_paste")
    job_desc = read_file(job_file) if job_file else job_text_area
    if job_file:
        st.success(f"✅ {job_file.name} loaded")

# 4. Analyze Button
if st.button("🚀 Analyze with 15 Models", type="primary", use_container_width=True):
    if resume_text.strip() and job_desc.strip():
        with st.spinner("15 HR Experts scanning... konjam wait pannu"):
            prompt = f"""
            You are 15 senior HR experts. Analyze Resume vs Job Description and give detailed feedback.

            RESUME:
            {resume_text}

            JOB DESCRIPTION:
            {job_desc}

            ### 1. OVERALL MATCH SCORE: XX/100
            ### 2. ATS KEYWORD MATCH
            ### 3. SKILLS GAP ANALYSIS
            ### 4. EXPERIENCE FIT
            ### 5. EDUCATION CHECK
            ### 6. PROJECT RELEVANCE
            ### 7. RESUME FORMATTING FEEDBACK
            ### 8. ACHIEVEMENT QUANTIFICATION TIPS
            ### 9. JOB ROLE ALIGNMENT %
            ### 10. INDUSTRY FIT
            ### 11. TOP 5 INTERVIEW QUESTIONS
            ### 12. SALARY BENCHMARK FOR INDIA
            ### 13. LINKEDIN PROFILE 3 TIPS
            ### 14. COVER LETTER 3 BULLET POINTS
            ### 15. 30-60-90 DAY PLAN
            """
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3500
            )
            st.success("### ✅ Analysis Complete")
            st.markdown(response.choices[0].message.content)
    else:
        st.warning("⚠️ Resume and JD rendu um podu da")

st.caption("Powered by Groq Llama-3.1-70B")
