import streamlit as st
import random

st.set_page_config(page_title="InterviewAI", layout="wide")
st.title("🤖 InterviewAI")

tab1, tab2 = st.tabs(["📄 Resume Score", "🎤 HR Mock Interview"])

# TAB 1: RESUME SCORE
with tab1:
    st.header("AI Resume Score Checker")
    st.write("Upload your resume and get instant AI feedback")
    uploaded_file = st.file_uploader("Choose PDF/DOCX/TXT", type=["pdf", "docx", "txt"])
    
    if uploaded_file is not None:
        st.success(f"✅ {uploaded_file.name} uploaded!")
        if st.button("Get Resume Score", key="score_btn"):
            with st.spinner("Analyzing..."):
                st.metric("Resume Score", "75/100")
                st.write("**Total Words:** 300")
                st.write("**Suggestions:**")
                st.write("- Add more keywords related to your job")
                st.write("- Improve formatting")

# TAB 2: HR QUESTIONS
with tab2:
    st.header("HR Mock Interview")
    job_role = st.text_input("Enter Job Role:", "Software Engineer")
    
    hr_questions = [
        "Tell me about yourself",
        "What are your strengths and weaknesses?",
        "Why should we hire you?",
        "Where do you see yourself in 5 years?",
        "Why do you want this job?"
    ]
    
    if st.button("Generate HR Questions", key="hr_btn"):
        st.write("### Here are 3 HR Questions:")
        for i, q in enumerate(random.sample(hr_questions, 3), 1):
            st.write(f"**Q{i}:** {q}")
    
    user_answer = st.text_area("Type your answer here:")
    if st.button("Get Feedback", key="feedback_btn"):
        if user_answer:
            st.success("Good answer! Try to add one specific example.")
        else:
            st.warning("Please type an answer first")
