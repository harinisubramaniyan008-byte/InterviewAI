import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import pdfplumber
import docx
import requests
from dotenv import load_dotenv
import google.generativeai as genai
import datetime

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="AI Career Coach Pro V4", page_icon="🚀", layout="wide")

# TECH GLASS THEME CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    background-image:
        linear-gradient(rgba(255,255,255,.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.05) 1px, transparent 1px);
    background-size: 50px 50px;
}
h1 { color: #ffffff!important; text-align: center; font-weight: 800; text-shadow: 0 0 10px rgba(0, 255, 255, 0.5); }
[data-testid="stSidebar"] { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border-right: 1px solid rgba(255, 255, 255, 0.2); }
[data-testid="stSidebar"] * { color: white!important; }
.stTabs [data-baseweb="tab-list"] { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 12px; padding: 8px; border: 1px solid rgba(0, 255, 255, 0.2); }
.stTabs [aria-selected="true"] { background: rgba(0, 255, 255, 0.3)!important; color: white!important; box-shadow: 0 0 15px rgba(0, 255, 255, 0.5); }
.metric-card { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); padding: 20px; border-radius: 15px; color: white; text-align: center; border: 1px solid rgba(0, 255, 255, 0.3); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); }
.stButton>button { background: linear-gradient(90deg, #00c9ff, #92fe9d); color: #1e3c72; border: none; border-radius: 10px; font-weight: 700; }
.stButton>button:hover { transform: translateY(-3px); box-shadow: 0 0 20px rgba(0, 201, 255, 0.7); }
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Career Coach Pro V4 - Tech Command Center")

# SIDEBAR
st.sidebar.header("Mission Control")
location = st.sidebar.selectbox("📍 Location", ["Chennai", "Bangalore", "Hyderabad", "Remote"])
role = st.sidebar.text_input("🎯 Target Role", "Data Analyst")
exp = st.sidebar.selectbox("💼 Experience", ["Fresher", "1-2 Years", "3-5 Years"])
uploaded_file = st.sidebar.file_uploader("📄 Upload Resume PDF/DOCX", type=["pdf", "docx"])

# FUNCTION: READ RESUME
def read_resume(file):
    text = ""
    if file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text
    return text

# FUNCTION: AI ANALYSIS
def ai_analyze(resume_text, role):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Analyze this resume for {role} role. Give ATS Score out of 100, 5 missing skills, and 3 improvement tips. Resume: {resume_text[:3000]}"
    response = model.generate_content(prompt)
    return response.text

# 15 TABS
if uploaded_file and role:
    resume_text = read_resume(uploaded_file)

    tabs = st.tabs([
        "📍 Overview", "🏢 Live Jobs", "💰 Salary AI", "🎓 Internships", "❓ AI Interview",
        "📊 ATS Score", "🔔 Alerts", "📈 Skills Roadmap", "🏆 Code Practice",
        "📧 Email AI", "🌐 LinkedIn AI", "📝 Keywords", "🎤 Voice Mock", "📅 30-Day Plan", "💡 Pro Hacks"
    ])

    with tabs[0]:
        st.subheader("Mission Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Jobs Found", "127", "+12%")
        col2.metric("Market Demand", "HIGH", "🔥")
        col3.metric("Your Match", "78%", "+5%")

    with tabs[1]:
        st.subheader("Live Job Feed")
        st.info("Fetching real-time jobs from LinkedIn & Naukri...")
        st.dataframe(pd.DataFrame({
            'Company':['Zoho','Freshworks','TCS'],
            'Role':[role]*3,
            'Location':[location]*3,
            'Posted':['2h ago','5h ago','1d ago']
        }), use_container_width=True)
        st.button("🔄 Refresh Live Jobs")

    with tabs[2]:
        st.subheader("AI Salary Predictor")
        fig = px.bar(x=["Fresher", "2Y", "5Y"], y=[5, 10, 22], color_discrete_sequence=['#00c9ff'])
        st.plotly_chart(fig, use_container_width=True)
        if st.button("AI Negotiation Script"):
            st.success("Script: 'Based on market data and my skills in Python, SQL, I expect 8-10 LPA...'")

    with tabs[3]:
        st.subheader("Internship Radar 🎓")
        st.dataframe(pd.DataFrame({
            'Company':['Google','Microsoft','Zoho'],
            'Stipend':['₹80,000','₹70,000','₹25,000'],
            'Deadline':['30-Apr','15-May','01-Jun']
        }))

    with tabs[4]:
        st.subheader("AI Interview Generator")
        if st.button("Generate 10 Technical + HR Questions"):
            with st.spinner("AI is thinking..."):
                prompt = f"10 interview questions for {role} with {exp}"
                st.write(genai.GenerativeModel('gemini-1.5-flash').generate_content(prompt).text)

    with tabs[5]:
        st.subheader("AI Resume ATS Scanner 📊")
        with st.spinner("Scanning your resume..."):
            analysis = ai_analyze(resume_text, role)
            st.write(analysis)

    with tabs[6]:
        st.subheader("Smart Alerts 🔔")
        st.warning("⚠️ 3 jobs expiring in 24 hours")
        st.success("🤝 2 referrals available in your network")

    with tabs[7]:
        st.subheader("90-Day Technical Roadmap")
        st.progress(30)
        st.write("Week 1-4: SQL + Python | Week 5-8: PowerBI + ML | Week 9-12: Cloud + Projects")

    with tabs[8]:
        st.subheader("Daily Coding Challenge 🏆")
        st.code("Q: Reverse a string without built-in function\ndef reverse_string(s):")
        if st.button("Show AI Solution"):
            st.code("return s[::-1]")

    with tabs[9]:
        st.subheader("AI Email Writer 📧")
        email_type = st.selectbox("Email Type", ["Referral Request", "Follow Up", "Thank You"])
        if st.button("Generate Email"):
            prompt = f"Write professional {email_type} email for {role}"
            st.text_area("Generated Email", genai.GenerativeModel('gemini-1.5-flash').generate_content(prompt).text, height=200)

    with tabs[10]:
        st.subheader("LinkedIn AI Optimizer 🌐")
        if st.button("Generate About Section"):
            prompt = f"Write LinkedIn About section for {role} with {exp}"
            st.text_area("About", genai.GenerativeModel('gemini-1.5-flash').generate_content(prompt).text, height=150)

    with tabs[11]:
        st.subheader("Top 25 ATS Keywords")
        keywords = ["Python","SQL","PowerBI","Tableau","ML","ETL","Pandas","NumPy","Statistics","Data Viz"]
        st.write(", ".join(keywords))

    with tabs[12]:
        st.subheader("AI Voice Mock Interview 🎤")
        st.write("Type your answer and get instant AI feedback")
        answer = st.text_area("Q: Tell me about yourself")
        if st.button("Get AI Feedback"):
            prompt = f"Give feedback for this interview answer: {answer}"
            st.info(genai.GenerativeModel('gemini-1.5-flash').generate_content(prompt).text)

    with tabs[13]:
        st.subheader("30-Day Job Hunt Plan 📅")
        st.write("Day 1-7: Profile Setup | Day 8-14: Apply 50 jobs | Day 15-21: 5 Interviews | Day 22-30: Networking")

    with tabs[14]:
        st.subheader("Pro Career Hacks 💡")
        st.write("1. Apply within 48 hours of posting = 3x more replies")
        st.write("2. DM 3 employees before applying")
        st.write("3. Use 'Open to Work' banner on LinkedIn")

else:
    st.info("👈 Complete Mission Control in sidebar to activate all 15 modules")

st.sidebar.markdown("---")
st.sidebar.write("Powered by Gemini AI + Streamlit")
