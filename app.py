import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Career Coach Pro", layout="wide")
st.title("🎯 AI Career Coach Pro - 15 Models")

# API Key
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("GOOGLE_API_KEY missing in Secrets")
    st.stop()

# Input
col1, col2 = st.columns(2)
with col1:
    resume_text = st.text_area("📄 Paste Resume", height=250)
with col2:
    job_desc = st.text_area("💼 Paste Job Description", height=250)

if st.button("🚀 Analyze with 15 Models", use_container_width=True):
    if resume_text and job_desc:
        with st.spinner("15 Models running... 20 seconds"):
            prompt = f"""
            You are 15 HR experts. Analyze this Resume vs Job Description and give output in 15 sections.

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
            response = model.generate_content(prompt)
            
            st.success("### ✅ Analysis Complete")
            st.markdown(response.text)
    else:
        st.warning("Resume and JD rendu um podu da")

st.sidebar.success("Powered by Gemini 1.5 Flash")
