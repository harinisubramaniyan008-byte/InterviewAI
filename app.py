import streamlit as st
from groq import Groq
import PyPDF2
import docx

st.set_page_config(page_title="AI Career Coach Pro", layout="wide")
st.title("🎯 AI Career Coach Pro - 15 Models")

# 1. GROQ API Key
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("GROQ_API_KEY missing in Secrets")
    st.stop()

# 2. File read panna function
def read_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    else:
        return uploaded_file.read().decode("utf-8")

# 3. Input - Upload + Text area rendu um
col1, col2 = st.columns(2)
with col1:
    st.subheader("📄 Resume")
    resume_file = st.file_uploader("Resume Upload Pannu", type=['pdf', 'docx', 'txt'])
    resume_text = st.text_area("Illa na inga Paste Pannu", height=200)
    if resume_file:
        resume_text = read_file(resume_file)

with col2:
    st.subheader("💼 Job Description")
    job_file = st.file_uploader("JD Upload Pannu", type=['pdf', 'docx', 'txt'])
    job_desc = st.text_area("Illa na inga Paste Pannu", height=200)
    if job_file:
        job_desc = read_file(job_file)

# 4. Button + 15 Models Output
if st.button("🚀 Analyze with 15 Models", type="primary", use_container_width=True):
    if resume_text and job_desc:
        with st.spinner("15 Models scanning... 15 seconds"):
            prompt = f"""
            You are 15 HR experts. Analyze this Resume vs Job Description.

            Resume: {resume_text}
            Job: {job_desc}

            ### 1. OVERALL SCORE
            Score: XX/100 with 2 line reason
            ### 2. ATS KEYWORD MATCH
            ### 3. SKILLS GAP ANALYSIS
            ### 4. EXPERIENCE FIT SCORE
            ### 5. EDUCATION CHECK
            ### 6. PROJECT RELEVANCE
            ### 7. RESUME FORMATTING FEEDBACK
            ### 8. ACHIEVEMENT QUANTIFICATION
            ### 9. JOB ROLE ALIGNMENT
            ### 10. INDUSTRY FIT
            ### 11. INTERVIEW QUESTIONS PREDICTED - 5
            ### 12. SALARY BENCHMARK
            ### 13. LINKEDIN PROFILE TIPS
            ### 14. COVER LETTER POINTS
            ### 15. 30-60-90 DAY PLAN
            """
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000
            )
            st.success("### ✅ Analysis Complete")
            st.markdown(response.choices[0].message.content)
    else:
        st.warning("Resume and JD rendu um podu da")
