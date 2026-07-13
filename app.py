import streamlit as st
from groq import Groq
import pdfplumber
import pandas as pd
import json
import re

st.set_page_config(page_title="AI Career OS PRO", layout="wide", page_icon="🚀", initial_sidebar_state="expanded")

st.markdown("""
<style>
.metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; text-align: center;}
.big-card {background-color: #FFFFFF; padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #E2E8F0;}
</style>
""", unsafe_allow_html=True)

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.sidebar.error("⚠️ Settings → Secrets la GROQ_API_KEY add pannu")
    st.stop()

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text(): text += page.extract_text() + "\n"
    return text

def ask_ai(prompt):
    with st.spinner("AI is thinking... 10-20 seconds"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "user", "content": prompt}], 
            temperature=0.3, 
            max_tokens=2500
        )
    return response.choices[0].message.content

def extract_json(text):
    # AI extra words kuduthalum JSON mattum edukum
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None
    return None

# SESSION STATE
if 'resume_text' not in st.session_state: st.session_state.resume_text = ""

# SIDEBAR
with st.sidebar:
    st.title("🚀 AI Career OS PRO v10.2")
    page = st.radio("Select Module", [
        "🏠 Dashboard", 
        "🧠 AI Doubt Clear - 24/7", 
        "💼 Live Mock Interview", 
        "🔎 AI Job + Course Finder", 
        "💻 Code + SQL Lab", 
        "🎯 Project Generator", 
        "📊 Skill Gap Analyzer"
    ])
    st.divider()
    st.header("Step 1: Upload Resume")
    resume_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    if resume_file:
        st.session_state.resume_text = read_pdf(resume_file)
        st.success("✅ Resume Loaded Successfully")

# PAGE 1: DASHBOARD - FIXED
if page == "🏠 Dashboard":
    st.title("AI Career Command Center")
    if st.session_state.resume_text == "":
        st.info("👈 Left la resume upload pannu. Illana Demo button adiku")
        if st.button("Load Demo Data"):
            st.session_state.resume_text = "John Doe, Python, SQL, Data Analyst, 2 years experience"
    else:
        if st.button("🚀 Analyze My Resume with AI", type="primary"):
            prompt = f"""
            Analyze this resume and return ONLY JSON. 
            Format: {{"ats_score": 80, "top_3_skills": ["Python","SQL"], "top_3_gaps": ["PowerBI","Cloud"], "summary": "2 line summary"}}
            RESUME: {st.session_state.resume_text[:4000]}
            """
            result = ask_ai(prompt)
            data = extract_json(result) # FIXED FUNCTION
            
            if data: # JSON KIDACHA
                col1, col2 = st.columns(2)
                with col1: st.metric("ATS Score", f"{data.get('ats_score',0)}/100")
                with col2: st.metric("Market Ready", f"{100-data.get('ats_score',0)}% Gap")
                st.progress(data.get('ats_score',0)/100)
                st.subheader("Your Top Skills"); st.write(data.get('top_3_skills',[]))
                st.subheader("Skills to Learn"); st.error(data.get('top_3_gaps',[]))
                st.info(data.get('summary',""))
            else: # JSON KIDAIKALA NA
                st.warning("AI returned text format. Here's the full analysis:")
                st.markdown(result) # RAW AH AZHAGA KAATUM. ERROR VARADHU

# PAGE 2: AI DOUBT CLEAR
elif page == "🧠 AI Doubt Clear - 24/7":
    st.title("🧠 Ask AI Anything - Like ChatGPT")
    st.write("Example: 'Explain Docker in Tamil with example'")
    doubt = st.text_area("Type your doubt here")
    if st.button("Get Answer from AI") and doubt:
        ans = ask_ai(f"Act as a senior tech mentor. Explain this clearly in Tamil + English mix with code example: {doubt}")
        st.markdown(ans)

# PAGE 3: LIVE MOCK INTERVIEW
elif page == "💼 Live Mock Interview":
    st.title("💼 AI Live Mock Interview")
    role = st.selectbox("Select Job Role", ["Data Analyst", "Python Developer", "Product Manager"])
    if st.button("Generate 5 Questions from My Resume"):
        qs = ask_ai(f"Generate 5 tough interview questions for {role} role based on this resume: {st.session_state.resume_text[:3000]}")
        st.session_state.qs = qs
        st.write(qs)

    ans = st.text_area("Type your answer here", height=200)
    if st.button("Get Real AI Score + Feedback") and ans:
        feedback = ask_ai(f"You are an HR. Question: {st.session_state.get('qs','N/A')}. My Answer: {ans}. Give score out of 10, 3 feedback points.")
        st.success(feedback)

# PAGE 4: JOB + COURSE FINDER
elif page == "🔎 AI Job + Course Finder":
    st.title("🔎 AI Job + Course Finder")
    search = st.text_input("What do you want? Ex: 'Python jobs in Chennai 5 LPA'")
    if st.button("Search with AI") and search:
        result = ask_ai(f"Find 5 real job roles and 3 best free YouTube courses for: {search}.")
        st.markdown(result)

# PAGE 5: CODE LAB
elif page == "💻 Code + SQL Lab":
    st.title("💻 Practice Code Here")
    lang = st.selectbox("Language", ["SQL", "Python"])
    code = st.text_area("Paste your code")
    if st.button("Explain Code Line by Line") and code:
        exp = ask_ai(f"Explain this {lang} code line by line for a beginner: {code}")
        st.code(code, language=lang.lower())
        st.info(exp)

# PAGE 6: PROJECT GENERATOR
elif page == "🎯 Project Generator":
    st.title("🎯 AI Project Ideas for Resume")
    if st.button("Generate 3 Resume Projects"):
        projects = ask_ai(f"Generate 3 unique resume projects for this person. Give Name, Tech Stack, 3 bullet points: {st.session_state.resume_text[:3000]}")
        st.markdown(projects)

# PAGE 7: SKILL GAP
elif page == "📊 Skill Gap Analyzer":
    st.title("📊 Skill Gap Analyzer")
    job = st.text_input("Target Job: Ex: 'Data Scientist'")
    if st.button("Analyze My Gap") and job:
        gap = ask_ai(f"Compare this resume vs {job} job. List missing skills and give 30 day learning roadmap: {st.session_state.resume_text[:3000]}")
        st.markdown(gap)
