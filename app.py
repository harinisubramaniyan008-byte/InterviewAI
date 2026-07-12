import streamlit as st
from groq import Groq
import pdfplumber
import docx

st.set_page_config(page_title="AI Career Coach Pro", layout="wide")
st.title("🎯 AI Career Coach Pro - 19 Models Analysis")

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
        text = uploaded_file.read().decode("utf-8", errors='ignore')
    return text

# 3. Input Section
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Resume Upload")
    resume_file = st.file_uploader("Upload Resume", type=['pdf', 'docx', 'txt'], key="resume_upload")
    resume_text_area = st.text_area("Illa na inga Paste Pannu", height=300, key="resume_paste")
    resume_text = read_file(resume_file) if resume_file else resume_text_area
    if resume_file:
        st.success(f"✅ {resume_file.name} loaded")

with col2:
    st.subheader("💼 Job Description Upload")
    job_file = st.file_uploader("Upload JD", type=['pdf', 'docx', 'txt'], key="jd_upload")
    job_text_area = st.text_area("JD ah inga Paste Pannu", height=300, key="jd_paste")
    job_desc = read_file(job_file) if job_file else job_text_area # idhu dhan cut aagiruchu
    if job_file:
        st.success(f"✅ {job_file.name} loaded")

st.markdown("---")

# 4. Analyze Button
if st.button("🚀 Analyze with 19 AI Models", type="primary", use_container_width=True):
    if resume_text.strip() and job_desc.strip():
        with st.spinner("19 AI Models scanning... 20 seconds wait pannu"):
            prompt = f"""You are 19 different HR experts, Recruiters, and ATS bots. Analyze this.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_desc}

Give output in this exact format:

### 🎯 1. OVERALL ATS SCORE: XX/100
### 📊 2. KEYWORD MATCH ANALYSIS
### 💪 3. SKILLS GAP ANALYSIS
### 🏆 4. EXPERIENCE RELEVANCE SCORE
### 🎓 5. EDUCATION ALIGNMENT
### 📈 6. PROJECT IMPACT SCORE
### 📝 7. RESUME FORMATTING & ATS COMPLIANCE
### 💰 8. ACHIEVEMENT QUANTIFICATION FEEDBACK
### 🎯 9. ROLE ALIGNMENT PERCENTAGE
### 🏢 10. INDUSTRY FIT ANALYSIS
### ❓ 11. TOP 10 PREDICTED INTERVIEW QUESTIONS
### 💵 12. SALARY BENCHMARK - INDIA
### 🔗 13. LINKEDIN OPTIMIZATION TIPS
### ✉️ 14. COVER LETTER KEY POINTS
### 📅 15. 30-60-90 DAY ACTION PLAN
### ⚠️ 16. RED FLAGS FOR RECRUITER
### 🚀 17. 3 QUICK WINS TO IMPROVE
### 📌 18. COMPETITOR CANDIDATE COMPARISON
### ✅ 19. FINAL HIRING RECOMMENDATION
"""
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.3
            )
            st.success("### ✅ 19 Models Analysis Complete!")
            st.markdown(response.choices[0].message.content)
    else:
        st.warning("⚠️ Resume and JD rendu um podu da")

st.caption("Powered by Groq Llama-3.1-70B | 19 AI HR Experts")
