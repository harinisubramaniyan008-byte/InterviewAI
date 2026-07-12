import streamlit as st
import pdfplumber
import docx
from groq import Groq
import json

# Page setup
st.set_page_config(page_title="AI Resume Interview", page_icon="📄")
st.title("📄 AI Resume + Interview App")

# Groq client - Secrets la irundhu key edukudhu
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Resume text extract panra function
def extract_text(uploaded_file):
    text = ""
    if uploaded_file.name.endswith(".pdf"):
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        text = uploaded_file.read().decode("utf-8")
    return text

# UI
uploaded_file = st.file_uploader("Upload your Resume", type=["pdf", "docx", "txt"])

if uploaded_file:
    resume_text = extract_text(uploaded_file)
    st.success("Resume Uploaded Successfully!")
    st.text_area("Extracted Resume Text", resume_text, height=200)

    if st.button("Get AI Resume Score"):
        with st.spinner("AI is analyzing your resume..."):
            prompt = f"""
            You are an HR expert. Analyze this resume and give:
            1. Overall Score out of 100
            2. 3 Strengths
            3. 3 Weaknesses
            4. 3 Suggestions to improve
            Resume: {resume_text}
            Give answer in JSON format.
            """

            try:
                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )

                result = response.choices[0].message.content
                st.subheader("AI Resume Analysis")
                st.write(result)

            except Exception as e:
                st.error(f"Error: {e}")
