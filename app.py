import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Career Coach Pro", layout="centered")
st.title("🎯 AI Career Coach Pro")

# 1. API Key direct ah Secrets la irundhu edukum
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("GOOGLE_API_KEY set pannala")
    st.stop()

# 2. Input
resume_text = st.text_area("📄 Resume Paste Pannu", height=200, placeholder="Unoda resume full ah paste pannu")
job_desc = st.text_area("💼 Job Description Paste Pannu", height=200, placeholder="Job JD paste pannu")

# 3. Button + 15 Models Output
if st.button("Analyze Now 🔥", type="primary", use_container_width=True):
    if resume_text and job_desc:
        with st.spinner("15 Models scanning..."):
            prompt = f"""
            Act as 15 HR experts. Give Overall Score/100 first.
            Then give 15 points: ATS, Skills Gap, Interview Q, etc.
            Keep it short. Use tables.

            Resume: {resume_text}
            JD: {job_desc}
            """
            res = model.generate_content(prompt)
            st.success("### Overall Score + 15 Model Report")
            st.write(res.text)
    else:
        st.warning("Rendu um fill pannu da")

st.caption("Powered by Gemini 1.5 Flash | No DB needed")
