import streamlit as st
from groq import Groq
import pdfplumber
import pandas as pd
import json
import re
import random # FOR GAME

st.set_page_config(page_title="AI Career OS PRO", layout="wide", page_icon="🚀", initial_sidebar_state="expanded")

st.markdown("""
<style>
.metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; text-align: center;}
.skill-tag {display:inline-block; background-color:#4F46E5; color:white; padding: 8px 15px; border-radius: 20px; margin: 5px; font-weight: 500;}
.gap-tag {display:inline-block; background-color:#EF4444; color:white; padding: 8px 15px; border-radius: 20px; margin: 5px; font-weight: 500;}
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
        response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], temperature=0.3, max_tokens=2500)
    return response.choices[0].message.content

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try: return json.loads(match.group())
        except: return None
    return None

if 'resume_text' not in st.session_state: st.session_state.resume_text = ""
if 'qs' not in st.session_state: st.session_state.qs = ""

# SIDEBAR
with st.sidebar:
    st.title("🚀 AI Career OS PRO v11.0")
    page = st.radio("Select Module", [
        "🏠 Dashboard",
        "🧠 AI Doubt Clear",
        "💼 Live Mock Interview",
        "🔎 AI Job + Course Finder",
        "💻 Code + SQL Lab",
        "🎯 Project Generator",
        "📊 Skill Gap Analyzer",
        "🎮 Daily Challenge",
        "🔥 Motivation Dose",
        "📈 Salary Calculator",
        "📚 7-Day Course Quest" # PUDHU IDHU
    ])
    st.divider()
    st.header("Step 1: Upload Resume")
    resume_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    if resume_file:
        st.session_state.resume_text = read_pdf(resume_file)
        st.success("✅ Resume Loaded")

# PAGE 1: DASHBOARD - PALAYA CODE + UI FIX
if page == "🏠 Dashboard":
    st.title("AI Career Command Center")
    if st.session_state.resume_text == "":
        st.info("👈 Left la resume upload pannu")
        if st.button("Load Demo Data"):
            st.session_state.resume_text = "Aspiring Design Engineer. Skills: Autocad 2D, Tekla Structures, STADD.pro"
    else:
        if st.button("🚀 Analyze My Resume with AI", type="primary"):
            prompt = f"""Analyze this resume and return ONLY JSON. Format: {{"ats_score": 80, "top_3_skills": ["Skill1","Skill2"], "top_3_gaps": ["Gap1","Gap2"], "summary": "2 line summary"}} RESUME: {st.session_state.resume_text[:4000]}"""
            result = ask_ai(prompt)
            data = extract_json(result)

            if data:
                col1, col2 = st.columns(2)
                with col1: st.markdown(f'<div class="metric-card"><h3>ATS Score</h3><h1>{data.get("ats_score",0)}/100</h1></div>', unsafe_allow_html=True)
                with col2: st.markdown(f'<div class="metric-card"><h3>Gap to Close</h3><h1>{100-data.get("ats_score",0)}%</h1></div>', unsafe_allow_html=True)
                st.progress(data.get('ats_score',0)/100)

                st.subheader("✅ Your Top Skills")
                for skill in data.get('top_3_skills',[]):
                    st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)

                st.subheader("🚀 Skills to Learn")
                for gap in data.get('top_3_gaps',[]):
                    st.markdown(f'<span class="gap-tag">{gap}</span>', unsafe_allow_html=True)

                with st.container(border=True):
                    st.subheader("AI Summary")
                    st.info(data.get('summary',""))
            else:
                st.warning("AI returned text format:")
                st.markdown(result)

# PAGE 2: AI DOUBT CLEAR - PALAYA CODE
elif page == "🧠 AI Doubt Clear":
    st.title("🧠 Ask AI Anything")
    doubt = st.text_area("Type your doubt here")
    if st.button("Get Answer from AI") and doubt:
        ans = ask_ai(f"Act as a senior tech mentor. Explain this clearly in Tamil + English mix with code example: {doubt}")
        st.markdown(ans)

# PAGE 3: MOCK INTERVIEW - PALAYA CODE
elif page == "💼 Live Mock Interview":
    st.title("💼 AI Live Mock Interview")
    role = st.selectbox("Select Job Role", ["Data Analyst", "Civil Engineer", "Python Developer"])
    if st.button("Generate 5 Questions"):
        qs = ask_ai(f"Generate 5 tough interview questions for {role} role based on this resume: {st.session_state.resume_text[:3000]}")
        st.session_state.qs = qs
        st.write(qs)
    ans = st.text_area("Type your answer here", height=200)
    if st.button("Get AI Score + Feedback") and ans:
        feedback = ask_ai(f"You are an HR. Question: {st.session_state.get('qs','N/A')}. My Answer: {ans}. Give score out of 10, 3 feedback points.")
        st.success(feedback)

# PAGE 4: JOB + COURSE FINDER - PALAYA CODE
elif page == "🔎 AI Job + Course Finder":
    st.title("🔎 AI Job + Course Finder")
    search = st.text_input("What do you want? Ex: 'Civil Engineer jobs in Chennai'")
    if st.button("Search with AI") and search:
        result = ask_ai(f"Find 5 real job roles and 3 best free YouTube courses for: {search}.")
        st.markdown(result)

# PAGE 5: CODE LAB - PALAYA CODE
elif page == "💻 Code + SQL Lab":
    st.title("💻 Practice Code Here")
    lang = st.selectbox("Language", ["SQL", "Python"])
    code = st.text_area("Paste your code")
    if st.button("Explain Code") and code:
        exp = ask_ai(f"Explain this {lang} code line by line for a beginner: {code}")
        st.code(code, language=lang.lower())
        st.info(exp)

# PAGE 6: PROJECT GENERATOR - PALAYA CODE
elif page == "🎯 Project Generator":
    st.title("🎯 AI Project Ideas for Resume")
    if st.button("Generate 3 Resume Projects"):
        projects = ask_ai(f"Generate 3 unique resume projects for this person. Give Name, Tech Stack, 3 bullet points: {st.session_state.resume_text[:3000]}")
        st.markdown(projects)

# PAGE 7: SKILL GAP - PALAYA CODE
elif page == "📊 Skill Gap Analyzer":
    st.title("📊 Skill Gap Analyzer")
    job = st.text_input("Target Job: Ex: 'Project Manager'")
    if st.button("Analyze My Gap") and job:
        gap = ask_ai(f"Compare this resume vs {job} job. List missing skills and give 30 day learning roadmap: {st.session_state.resume_text[:3000]}")
        st.markdown(gap)

# PAGE 8: DAILY CHALLENGE - CREATIVE
elif page == "🎮 Daily Challenge":
    st.title("🎮 Daily Career Quest")
    st.write("Complete today’s mission and earn XP!")

    challenges = [
        "Update 1 bullet point in your resume with a number. Ex: 'Increased speed by 30%'",
        "Learn 1 new SQL query and test it",
        "Connect with 1 person on LinkedIn in your target company",
        "Watch 10 min of a PowerBI tutorial",
        "Rewrite your LinkedIn Headline"
    ]
    today_challenge = random.choice(challenges)

    with st.container(border=True):
        st.subheader("Today's Mission")
        st.info(f"🔥 {today_challenge}")
        if st.checkbox("I Completed This!"):
            st.success("Congrats! +50 XP Earned")
            st.balloons()
    st.progress(0.65, text="Level 5: Career Grinder - 650 XP")

# PAGE 9: MOTIVATION DOSE - CREATIVE
elif page == "🔥 Motivation Dose":
    st.title("🔥 AI Motivation + Meme Generator")
    st.write("Feeling low? Click and get fired up!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Give Me Motivation 💪"):
            moti = ask_ai("Give 1 line hardcore motivation for a job seeker in Tamil + English mix")
            st.success(moti)
    with col2:
        if st.button("Give Me a Career Meme 😂"):
            meme = ask_ai("Give 1 funny career meme line about 'resume rejection' in Tamil + English mix")
            st.warning(meme)

# PAGE 10: SALARY CALCULATOR - CREATIVE
elif page == "📈 Salary Calculator":
    st.title("📈 'What If' Salary Calculator")
    st.write("Learn a skill and see your salary jump!")

    current_salary = st.number_input("Enter Current Salary in LPA", value=4.0, step=0.5)
    skill = st.selectbox("If I learn this skill", ["PowerBI", "Machine Learning", "Cloud AWS", "Project Management", "Revit"])

    if st.button("Calculate My New Salary"):
        hike = ask_ai(f"If a Civil Engineer with {current_salary} LPA salary learns {skill}, what is the average salary hike % in India 2026? Give answer in 1 line with new salary.")
        st.metric("AI Prediction", hike)
        st.info("Note: This is AI estimation based on market data")

# PAGE 11: 7-DAY COURSE QUEST - PUDHU MODULE
elif page == "📚 7-Day Course Quest":
    st.title("📚 7-Day Course Quest")
    st.write("Pick 1 Course. AI will give you full roadmap + daily tasks with XP")

    course = st.selectbox("Choose Your Course", [
        "PowerBI for Beginners",
        "Python for Data Analysis",
        "SQL Mastery",
        "Revit Architecture Basics",
        "Project Management with MS Project"
    ])

    if st.button("Generate My 7-Day Roadmap", type="primary"):
        with st.spinner("AI is creating your personal course..."):
            prompt = f"""
            For the course '{course}', generate JSON only.
            Format: {{
            "overview": "2 line what you will learn",
            "tools": ["Tool1", "Tool2"],
            "project": "1 final project idea",
            "tasks": [
                {{"day": 1, "task": "Task 1", "xp": 50}},
                {{"day": 2, "task": "Task 2", "xp": 50}},
                {{"day": 3, "task": "Task 3", "xp": 50}},
                {{"day": 4, "task": "Task 4", "xp": 50}},
                {{"day": 5, "task": "Task 5", "xp": 50}},
                {{"day": 6, "task": "Task 6", "xp": 50}},
                {{"day": 7, "task": "Final Project + Portfolio Update", "xp": 100}}
            ]
            }}
            """
            result = ask_ai(prompt)
            data = extract_json(result)

        if data:
            st.success(f"Roadmap Generated for: {course}")

            col1, col2, col3 = st.columns(3)
            with col1:
                with st.container(border=True):
                    st.subheader("🎯 What You'll Learn")
                    st.write(data.get("overview"))
            with col2:
                with st.container(border=True):
                    st.subheader("🛠️ Tools Used")
                    for tool in data.get("tools",[]):
                        st.markdown(f'- {tool}')
            with col3:
                with st.container(border=True):
                    st.subheader("🏆 Final Project")
                    st.write(data.get("project"))

            st.divider()
            st.subheader("🗓️ Your 7 Day Task List")

            total_xp = 0
            for task in data.get("tasks", []):
                with st.container(border=True):
                    colA, colB = st.columns([0.8, 0.2])
                    with colA:
                        st.markdown(f"**Day {task['day']}:** {task['task']}")
                        if st.checkbox(f"Mark Day {task['day']} Complete", key=f"day{task['day']}"):
                            st.success(f"+{task['xp']} XP Earned!")
                            total_xp += task['xp']
                    with colB:
                        st.metric("XP", f"+{task['xp']}")

            st.progress(total_xp/450, text=f"Course Progress: {total_xp}/450 XP")
        else:
            st.warning("AI returned text. Here's the roadmap:")
            st.markdown(result)
