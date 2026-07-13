import streamlit as st
from groq import Groq
import pdfplumber
from docx import Document
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="AI Career Coach 2.0", layout="wide")

st.title("🤖 AI Career Coach 2.0")
st.write("Upload your Resume. Get Instant ATS Score, Company List, Salary, and Learning Path.")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Please add GROQ_API_KEY in Streamlit Secrets")
    st.stop()

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def get_ai_analysis(resume_text, location):
    prompt = f"""
    You are a Senior AI Career Coach and Market Analyst. Be professional, technical, and data-driven.

    RESUME:
    {resume_text}

    TARGET LOCATION: {location}

    Analyze and return output in professional English with clear headings.

    **MODULE 1: INSTANT ATS SCORE**
    Give score /100 and show breakdown: Keywords, Experience, Format, Education. Also provide a JSON for radar chart: {{"Keywords": 80, "Experience": 60,...}}

    **MODULE 2: AI FEEDBACK**
    3 Key Strengths, 3 Critical Weaknesses, 3 Immediate Actions to Fix

    **MODULE 3: TOP COMPANIES IN {location}**
    List 10 companies hiring for roles matching this resume. Include Company Name, Why they fit, and 1 line about them.

    **MODULE 4: SKILL GAP & LEARNING PATH**
    Top 5 Missing Skills. For each: Why it matters + 1 Free Course Link + 1 Paid Course Link

    **MODULE 5: SALARY BENCHMARK FOR {location}**
    For top 3 matching roles. Give Fresher, 2-4 Years, 5+ Years salary range in INR

    **MODULE 6: TOP 15 INTERVIEW QUESTIONS**
    10 Technical + 5 HR questions predicted for this profile

    **MODULE 7: RESUME REWRITE SUGGESTION**
    Pick 3 weak bullet points from resume and rewrite them with metrics and action verbs

    **MODULE 8: BEST JOB MATCHES**
    Top 5 Job Titles this person fits for with Match %

    **MODULE 9: LINKEDIN & NETWORKING STRATEGY**
    3 steps to get noticed by recruiters in {location}

    **MODULE 10: MARKET TREND**
    Is demand for this profile increasing or decreasing? 1 key trend for 2026

    Be specific. No generic advice.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are a professional AI Career Coach."},
                  {"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=4000
    )
    return response.choices[0].message.content

# UI
col1, col2 = st.columns([2,1])
with col1:
    resume_file = st.file_uploader("1. Upload Your Resume PDF/DOCX", type=["pdf", "docx", "txt"])
with col2:
    location = st.selectbox("2. Select Your Target Location", ["Chennai", "Bangalore", "Hyderabad", "Pune", "Mumbai", "Remote"])

if st.button("🚀 Generate Full Career Report"):
    if resume_file:
        with st.spinner("AI is analyzing your profile... This takes 30 seconds"):
            if resume_file.type == "application/pdf":
                resume_text = read_pdf(resume_file)
            elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = read_docx(resume_file)
            else:
                resume_text = resume_file.read().decode("utf-8")

            result = get_ai_analysis(resume_text, location)
            st.success("✅ Report Generated Successfully!")
            st.markdown(result)
    else:
        st.warning("Please upload your resume first")
