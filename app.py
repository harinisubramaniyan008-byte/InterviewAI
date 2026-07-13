import streamlit as st
from groq import Groq
import pdfplumber # PyPDF2 illai
from docx import Document
import io

st.set_page_config(page_title="AI Career Coach", layout="wide")

st.title("🤖 AI Career Coach")
st.write("Resume ah upload pannu, JD podu. Analyze pannalam")

# API Key
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("GROQ_API_KEY set pannala. Streamlit Secrets la add pannu")
    st.stop()

# File upload functions - IDHU MAATHITEN
def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def read_docx(file):
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def read_txt(file):
    return file.read().decode("utf-8")

# Main function
def analyze_resume(resume_text, jd_text):
    prompt = f"""
    You are an expert AI Career Coach and ATS Scanner.

    Resume:
    {resume_text}

    Job Description:
    {jd_text}

    Task:
    1. Give Overall ATS Score out of 100
    2. List Top 5 Matching Skills
    3. List Top 5 Missing Skills
    4. Give 3 Improvement Suggestions

    Format it clearly with headings.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # IMPORTANT: 3.1 illa 3.3
        messages=[
            {"role": "system", "content": "You are a helpful AI career coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=2000
    )
    return response.choices[0].message.content

# UI
col1, col2 = st.columns(2)

with col1:
    st.subheader("Step 1: Resume Upload")
    resume_file = st.file_uploader("Upload Resume PDF/DOCX/TXT", type=["pdf", "docx", "txt"])

with col2:
    st.subheader("Step 2: Job Description")
    jd_text = st.text_area("Paste Job Description here", height=200)

if st.button("🚀 Analyze Pannu"):
    if resume_file and jd_text:
        with st.spinner("Analyzing... Konjam time aagum"):
            # Read resume
            if resume_file.type == "application/pdf":
                resume_text = read_pdf(resume_file)
            elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = read_docx(resume_file)
            else:
                resume_text = read_txt(resume_file)

            # Call Groq
            try:
                result = analyze_resume(resume_text, jd_text)
                st.success("Analysis Complete!")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Resume + JD rendu um podu da")
