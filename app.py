import streamlit as st
from groq import Groq
import pdfplumber
from docx import Document

st.set_page_config(page_title="AI Career Coach PRO", layout="wide")
st.title("🤖 AI Career Coach PRO")
st.write("Resume mattum upload pannu. AI eh role ah guess panni 15 modules la analyze pannum")

# API Key
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("GROQ_API_KEY set pannala")
    st.stop()

# File readers
def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_txt(file):
    return file.read().decode("utf-8")

# AI AUTO JD + ANALYSIS PROMPT
def analyze_resume_auto(resume_text):
    prompt = f"""
    You are a Senior Tech Recruiter + Career Coach.

    RESUME:
    {resume_text}

    TASK:
    Step 1: First, analyze this resume and GUESS the best 3 job roles this person fits for.
    Pick the BEST 1 role and CREATE a detailed Job Description for it with Required Skills.

    Step 2: Now compare this resume AGAINST the JD you just created and give output in 15 MODULES:

    **MODULE 1: AI GUESS ROLE + GENERATED JD**
    Show the role name + Full JD with 5 responsibilities + 8 required skills

    **MODULE 2: ATS SCORE** /100 + Breakdown

    **MODULE 3: KEYWORD MATCH**
    20 keywords from AI JD. [MATCHED]/[MISSING]

    **MODULE 4: TECHNICAL SKILLS GAP TABLE**
    Required vs Have vs Proficiency 1-5

    **MODULE 5: PROJECT RELEVANCE**
    Top 3 projects. Score /10 + 1 improvement line each

    **MODULE 6: TOP 10 MISSING SKILLS**
    Why each skill matters for this role

    **MODULE 7: STRONG vs WEAK VERBS**

    **MODULE 8: QUANTIFIABLE ACHIEVEMENTS MISSING**
    Give 3 examples with % or $

    **MODULE 9: CERTIFICATION SUGGESTIONS**
    3 certifications to get this job

    **MODULE 10: TOOLS RATING**
    Python, SQL, PowerBI, Tableau, Excel 1-5

    **MODULE 11: RESUME FORMATTING SCORE** + Fixes

    **MODULE 12: 10 PREDICTED INTERVIEW QUESTIONS**

    **MODULE 13: 30-60-90 DAY PLAN**

    **MODULE 14: INDIA SALARY BENCHMARK**

    **MODULE 15: FINAL VERDICT + 3 PRIORITY ACTIONS**

    Be BRUTAL and TECHNICAL. No fluff.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a brutally honest senior tech recruiter."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=4000
    )
    return response.choices[0].message.content

# UI - JD BOX REMOVE PANNITEN
st.subheader("Step 1: Resume Upload")
resume_file = st.file_uploader("Upload Resume PDF/DOCX/TXT", type=["pdf", "docx", "txt"])

if st.button("🚀 AI Auto Analyze Pannu"):
    if resume_file:
        with st.spinner("AI is guessing your role + Deep Scan... 30 sec"):
            # Read resume
            if resume_file.type == "application/pdf":
                resume_text = read_pdf(resume_file)
            elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = read_docx(resume_file)
            else:
                resume_text = read_txt(resume_file)

            try:
                result = analyze_resume_auto(resume_text)
                st.success("✅ Analysis Complete!")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Resume ah first upload pannu da")
