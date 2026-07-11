import streamlit as st
import pandas as pd
import PyPDF2
from docx import Document

st.set_page_config(page_title="InterviewAI", layout="wide")
st.title("🤖 InterviewAI - AI Resume Score Checker")
st.write("Upload your resume and get instant AI feedback")

uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    st.success(f"✅ {uploaded_file.name} uploaded successfully!")
    
    if st.button("Get Resume Score"):
        with st.spinner("Analyzing your resume..."):
            # Sample scoring - nee unoda logic inga podalam
            st.metric("Resume Score", "75/100")
            st.write("**Total Words:** 300")
            st.write("**Suggestions:**")
            st.write("- Add more keywords related to your job")
            st.write("- Improve formatting")
