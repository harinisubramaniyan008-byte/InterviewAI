import streamlit as st
import random

st.set_page_config(page_title="InterviewAI", layout="wide")
st.title("🤖 InterviewAI")

tab1, tab2 = st.tabs(["📄 Resume Score", "🎤 HR Mock Interview"])

with tab1:
    st.header("AI Resume Score Checker")
    uploaded_file = st.file_uploader("Choose PDF/DOCX/TXT", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        st.success(f"✅ {uploaded_file.name} uploaded!")
        if st.button("Get Resume Score"):
            st.metric("Resume Score", "75/100")
            st.write("**Feedback:** Good resume! Add more keywords.")

with tab2:
    st.header("HR Mock Interview")
    job_role = st.text_input("Enter Job Role:", "Software Engineer")
    if st.button("Generate HR Questions"):
        questions = [
            "Tell me about yourself",
            "Why do you want this job?", 
            "What are your strengths?"
        ]
        for i, q in enumerate(questions, 1):
            st.write(f"**Q{i}:** {q}")
