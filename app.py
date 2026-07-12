import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import pdfplumber
import docx
from dotenv import load_dotenv
import google.generativeai as genai
import datetime

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="AI Career Coach Pro", page_icon="🚀", layout="wide")

# NORMAL CLEAN PROFESSIONAL THEME
st.markdown("""
<style>
.stApp { background-color: #ffffff; }
h1 { color: #1a365d!important; text-align: center; font-weight: 700; }
[data-testid="stSidebar"] { background-color: #f7fafc; border-right: 1px solid #e2e8f0; }
[data-testid="stSidebar"] * { color: #2d3748!important; }
.stTabs [data-baseweb="tab-list"] { background-color: #f7fafc; border-radius: 8px; }
.stTabs [aria-selected="true"] { background-color: #2b6cb0!important; color: white!important; border-radius: 6px; font-weight: 600; }
.metric-card { background: #ffffff; padding: 20px; border-radius: 8px; color: #2d3748; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.stButton>button { background-color: #2b6cb0; color: white; border: none; border-radius: 6px; font-weight: 600; }
.stButton>button:hover { background-color: #2c5282; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Career Coach Pro")

# SIDEBAR
st.sidebar.header("Your Profile")
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

# 15 TABS
if uploaded_file and role:
    resume_text = read_resume(uploaded_file)

    tabs = st.tabs([
        "📍 Overview", "🏢 Companies", "💰 Salary", "🎓 Internships", "❓ AI Interview",
        "📊 ATS Score", "🔔 Alerts", "📈 Skills Roadmap", "🏆 Code Practice",
        "📧 Email AI", "🌐 LinkedIn AI", "📝 Keywords", "🎤 Mock Interview", "📅 30-Day Plan", "💡 Pro Tips"
    ])

    with tabs[0]:
        st.subheader("Dashboard Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="metric-card"><h3>Jobs Found</h3><h2>127</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card"><h3>Market Demand</h3><h2>HIGH 🔥</h2></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card"><h3>Your Match</h3><h2>78%</h2></div>', unsafe_allow_html=True)

    with tabs[1]:
        st.subheader("Top Companies Hiring")
        companies_df = pd.DataFrame({
            'Company':['TCS','Zoho','Freshworks','Infosys','Wipro'],
            'Role':[role]*5, 'Location':[location]*5, 'Openings':[12,5,8,10,7]
        })
        st.dataframe(companies_df, use_container_width=True)

    with tabs[2]:
        st.subheader("Salary Predictor")
        col1, col2, col3 = st.columns(3)
        col1.metric("Fresher", "₹3.6 - ₹6 LPA")
        col2.metric("2 Yrs Exp", "₹8 - ₹12 LPA")
        col3.metric("5 Yrs Exp", "₹15 - ₹25 LPA")
        fig = px.bar(x=["Fresher", "2Y", "5Y"], y=[4.5, 10, 20], title="Salary Growth")
        st.plotly_chart(fig, use_container_width=True)

    with tabs[3]:
        st.subheader("Latest Internships")
        st.dataframe(pd.DataFrame({
            'Company':['Zoho','Google','Microsoft'],
            'Role':['Data Intern','AI Intern','Product Intern'],
            'Stipend':['₹25,000','₹80,000','₹70,000'],
            'Deadline':['30-Apr-2026','15-May-2026','01-Jun-2026']
        }), use_container_width=True)

    with tabs[4]:
        st.subheader("AI Interview Questions")
        if st.button("Generate 10 Questions"):
            with st.spinner("Generating..."):
                prompt = f"Generate 10 interview questions for {role} with {exp} experience"
                model = genai.GenerativeModel('gemini-1.5-flash')
                st.write(model.generate_content(prompt).text)

    with tabs[5]:
        st.subheader("ATS Resume Score")
        with st.spinner("Analyzing your resume..."):
            prompt = f"Analyze this resume for {role} role. Give ATS Score out of 100, 5 missing skills, and 3 improvement tips. Resume: {resume_text[:2000]}"
            model = genai.GenerativeModel('gemini-1.5-flash')
            st.write(model.generate_content(prompt).text)

    with tabs[6]:
        st.subheader("Job Alerts")
        st.warning("⚠️ TCS Drive - Last 48 hours to apply!")
        st.info("📧 3 new jobs matched your profile today")
        st.success("🤝 2 referrals available in your network")

    with tabs[7]:
        st.subheader("90-Day Skills Roadmap")
        st.progress(30)
        st.write("**Month 1**: SQL + Excel | **Month 2**: PowerBI + Python | **Month 3**: ML + Cloud")

    with tabs[8]:
        st.subheader("Daily Coding Practice")
        st.code("Q: Find Second Largest Element in Array")
        if st.button("Show Solution"):
            st.code("def second_largest(arr):\n return sorted(set(arr))[-2]")

    with tabs[9]:
        st.subheader("AI Email Writer")
        email_type = st.selectbox("Email Type", ["Referral Request", "Follow Up", "Thank You"])
        if st.button("Generate Email"):
            prompt = f"Write professional {email_type} email for {role}"
            model = genai.GenerativeModel('gemini-1.5-flash')
            st.text_area("Generated Email", model.generate_content(prompt).text, height=200)

    with tabs[10]:
        st.subheader("LinkedIn Profile Optimizer")
        if st.button("Generate About Section"):
            prompt = f"Write LinkedIn About section for {role} with {exp}"
            model = genai.GenerativeModel('gemini-1.5-flash')
            st.text_area("About", model.generate_content(prompt).text, height=150)

    with tabs[11]:
        st.subheader("Top 20 ATS Keywords")
        st.write(", ".join(["Python","SQL","PowerBI","Tableau","Machine Learning","Data Visualization","ETL","Pandas","NumPy","Statistics","Analytics","Dashboard","Big Data","Cloud","API"]))

    with tabs[12]:
        st.subheader("AI Mock Interview")
        answer = st.text_area("Q: Tell me about yourself for a Data Analyst role")
        if st.button("Get AI Feedback"):
            prompt = f"Give feedback for this interview answer: {answer}"
            model = genai.GenerativeModel('gemini-1.5-flash')
            st.info(model.generate_content(prompt).text)

    with tabs[13]:
        st.subheader("30-Day Job Hunt Plan")
        st.write("**Week 1**: Update Resume + LinkedIn | **Week 2**: Apply to 50 jobs | **Week 3**: 5 Mock Interviews | **Week 4**: Networking + Followups")

    with tabs[14]:
        st.subheader("Pro Career Tips")
        st.write("1. Apply within 48 hours of job posting")
        st.write("2. Connect with 3 employees before applying")
        st.write("3. Use 'Easy Apply' on LinkedIn for 3x more responses")

else:
    st.info("👈 Please complete your profile in the sidebar to activate all 15 modules")

st.sidebar.markdown("---")
st.sidebar.write("Powered by Gemini AI")
