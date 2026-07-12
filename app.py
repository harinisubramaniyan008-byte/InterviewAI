import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Career Coach Pro", layout="wide")
st.title("🎯 AI Career Coach Pro - 15 Models")

# 1. GROQ API Key - idha dhan ipo use pannaporom
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("GROQ_API_KEY missing in Secrets")
    st.stop()

# 2. Input
col1, col2 = st.columns(2)
with col1:
    resume_text = st.text_area("📄 Resume Paste Pannu", height=250)
with col2:
    job_desc = st.text_area("💼 Job Description Paste Pannu", height=250)

# 3. Button + 15 Models Output
if st.button("🚀 Analyze with 15 Models", type="primary", use_container_width=True):
    if resume_text and job_desc:
        with st.spinner("15 Models scanning... 15 seconds"):
            prompt = f"""
            You are 15 HR experts. Analyze this Resume vs Job Description.

            Resume: {resume_text}
            Job: {job_desc}

            Give output like this:

            ### 1. OVERALL SCORE
            Score: XX/100 with 2 line reason

            ### 2. ATS KEYWORD MATCH
            Matched: list 10
            Missing: list 10

            ### 3. SKILLS GAP ANALYSIS
            ### 4. EXPERIENCE FIT SCORE
            ### 5. EDUCATION CHECK
            ### 6. PROJECT RELEVANCE
            ### 7. RESUME FORMATTING FEEDBACK
            ### 8. ACHIEVEMENT QUANTIFICATION
            ### 9. JOB ROLE ALIGNMENT
            ### 10. INDUSTRY FIT
            ### 11. INTERVIEW QUESTIONS PREDICTED - give 5
            ### 12. SALARY BENCHMARK
            ### 13. LINKEDIN PROFILE TIPS
            ### 14. COVER LETTER POINTS
            ### 15. 30-60-90 DAY PLAN

            Keep it short, bullet points, table format where possible.
            """
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=3000
            )

            st.success("### ✅ Analysis Complete")
            st.markdown(response.choices[0].message.content)
    else:
        st.warning("Resume and JD rendu um podu da")

st.sidebar.success("Powered by Llama 3.1 70B via Groq")
