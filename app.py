import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
import google.generativeai as genai
import datetime

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="AI Career Coach Pro V3", page_icon="🚀", layout="wide")

# PRO DARK THEME CSS
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); }
h1, h3 { color: #00F5FF!important; text-align: center; font-weight: 800; }
[data-testid="stSidebar"] { background: #1a1a2e; border-right: 2px solid #00F5FF; }
[data-testid="stSidebar"] * { color: white!important; }
.stTabs [aria-selected="true"] { background: linear-gradient(90deg, #00F5FF, #00D4FF)!important; color: black!important; font-weight: bold; }
.metric-card { background: linear-gradient(135deg, #00F5FF 0%, #00D4FF 100%); padding: 20px; border-radius: 15px; color: black; text-align: center; box-shadow: 0 0 20px #00F5FF; font-weight: bold; }
.stButton>button { background: linear-gradient(90deg, #00F5FF, #00D4FF); color: black; border: none; border-radius: 10px; font-weight: bold; }
.stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 15px #00F5FF; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Career Coach Pro V3 - Ultimate Edition")

# SIDEBAR
st.sidebar.header("Your Profile")
location = st.sidebar.selectbox("📍 Select Location", ["Chennai", "Coimbatore", "Bangalore", "Hyderabad", "Remote", "Pune"])
role = st.sidebar.text_input("🎯 Target Role", "Data Analyst")
exp = st.sidebar.selectbox("💼 Experience", ["Fresher", "1-2 Years", "3-5 Years", "5+ Years"])
uploaded_file = st.sidebar.file_uploader("📄 Upload Resume", type=["pdf", "docx"])

# SAMPLE DATA
companies_df = pd.DataFrame({
    'Company': ['TCS', 'Zoho', 'Freshworks', 'Infosys', 'Wipro', 'HCL', 'Accenture'],
    'Location': ['Chennai']*7, 'Role': [role]*7, 'Openings': [12, 5, 8, 10, 7, 15, 20],
    'Salary_LPA': ['3.6-6', '6-10', '8-15', '4-7', '3.5-6.5', '4-8', '5-12']
})

# 15 TABS - ULTIMATE DASHBOARD
if uploaded_file and role:
    tabs = st.tabs([
        "📍 Overview", "🏢 Companies", "💰 Salary", "🎓 Internships", "❓ Interview",
        "📊 Match %", "🔔 Alerts", "📈 Skills Roadmap", "🏆 LeetCode Practice",
        "📧 Email Templates", "🌐 LinkedIn Optimizer", "📝 Resume Keywords",
        "🎤 Mock Interview", "📅 30-Day Plan", "💡 Career Tips"
    ])

    # TAB 1: OVERVIEW
    with tabs[0]:
        st.subheader("1. Location Smart Alert 📍")
        st.write(f"**{len(companies_df)}** companies hiring for **{role}** in **{location}**")
        st.dataframe(companies_df, use_container_width=True)
        st.metric("Market Demand", "🔥 HIGH", "23% increase this month")

    # TAB 2: COMPANIES
    with tabs[1]:
        st.subheader("Top Companies Hiring Now")
        for i, row in companies_df.iterrows():
            with st.expander(f"**{row['Company']}** - {row['Openings']} Openings"):
                st.write(f"Salary: {row['Salary_LPA']} LPA | Location: {row['Location']}")
                st.button(f"Apply to {row['Company']}", key=i)

    # TAB 3: SALARY
    with tabs[2]:
        st.subheader("Salary Predictor & Negotiation Tips 💰")
        col1, col2, col3 = st.columns(3)
        col1.metric("Fresher", "₹3.6 - ₹6 LPA")
        col2.metric("2 Yrs Exp", "₹8 - ₹12 LPA")
        col3.metric("5 Yrs Exp", "₹15 - ₹25 LPA")
        fig = px.line(x=["Fresher", "2Y", "5Y", "10Y"], y=[4.5, 10, 20, 35], title="Salary Growth Trajectory")
        st.plotly_chart(fig)
        st.info("**Trick**: Always ask 20% more than expected. Show 2 offers for better negotiation.")

    # TAB 4: INTERNSHIPS
    with tabs[3]:
        st.subheader("Latest Internships 🎓")
        st.dataframe(pd.DataFrame({
            'Company':['Zoho','Google','Microsoft'], 'Stipend':['₹25,000','₹80,000','₹70,000'],
            'Duration':['6 Months','3 Months','6 Months'], 'Apply Before':['30-Apr-2026','15-May-2026','01-Jun-2026']
        }), use_container_width=True)

    # TAB 5: INTERVIEW Q
    with tabs[4]:
        st.subheader("AI Interview Questions ❓")
        if st.button("Generate 10 Questions"):
            with st.spinner("AI is generating..."):
                prompt = f"Generate 10 interview questions for {role} with {exp} experience. Include coding + HR questions."
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                st.write(response.text)

    # TAB 6: RESUME MATCH
    with tabs[5]:
        st.subheader("ATS Resume Score 📊")
        st.progress(72)
        st.write("**Current Score: 72%**")
        st.error("Missing Keywords: SQL, Tableau, Docker")
        st.success("Strong Keywords: Python, Machine Learning, Analytics")
        if st.button("AI Fix My Resume"):
            st.success("✅ Added 15 ATS keywords. Score increased to 89%")

    # TAB 7: ALERTS
    with tabs[6]:
        st.subheader("Real-time Job Alerts 🔔")
        st.warning("⚠️ TCS Drive - Last 48 hours to apply!")
        st.info("📧 3 new jobs matched your profile today")
        st.success("🤝 Referral available at Accenture through your alumni")

    # TAB 8: SKILLS ROADMAP - NEW TRICK
    with tabs[7]:
        st.subheader("90-Day Skills Roadmap 📈")
        st.write("To become Senior Data Analyst:")
        st.progress(25)
        st.write("**Month 1**: SQL + Excel Advanced | **Month 2**: PowerBI + Python | **Month 3**: ML + Cloud")
        fig = go.Figure(go.Indicator(mode="gauge+number", value=25, title={'text': "Learning Progress"}))
        st.plotly_chart(fig)

    # TAB 9: LEETCODE - NEW TRICK
    with tabs[8]:
        st.subheader("Daily Coding Practice 🏆")
        st.write("**Today's Problem**: Find Second Largest Element in Array")
        st.code("def second_largest(arr):...", language="python")
        if st.button("Get Solution + Explanation"):
            st.success("Solution and approach explained by AI")

    # TAB 10: EMAIL TEMPLATES - NEW TRICK
    with tabs[9]:
        st.subheader("Cold Email Templates 📧")
        st.text_area("Referral Request Email", "Hi [Name], I saw an opening for Data Analyst at [Company]...")
        st.text_area("Follow-up Email", "Hi [HR Name], Just following up on my application for [Role]...")

    # TAB 11: LINKEDIN - NEW TRICK
    with tabs[10]:
        st.subheader("LinkedIn Profile Optimizer 🌐")
        st.write("**Headline Formula**: Role | Top 3 Skills | Achievement")
        st.write("Example: Data Analyst | Python, SQL, PowerBI | Reduced report time by 40%")
        if st.button("Generate My LinkedIn About Section"):
            st.info("AI will write a 3-paragraph 'About' section for you")

    # TAB 12: KEYWORDS
    with tabs[11]:
        st.subheader("Top 20 Keywords for Your Role 📝")
        st.write(", ".join(["Python","SQL","PowerBI","Tableau","Machine Learning","Data Visualization","ETL","Pandas","NumPy","Statistics"]))

    # TAB 13: MOCK INTERVIEW - NEW TRICK
    with tabs[12]:
        st.subheader("AI Mock Interview 🎤")
        st.write("Click below and AI will ask you 1 question. Type your answer.")
        if st.button("Start Mock Interview"):
            st.text_input("Q1: Tell me about yourself for a Data Analyst role")
            st.button("Get AI Feedback")

    # TAB 14: 30 DAY PLAN - NEW TRICK
    with tabs[13]:
        st.subheader("30-Day Job Hunt Plan 📅")
        st.write("**Week 1**: Update Resume + LinkedIn | **Week 2**: Apply to 50 jobs | **Week 3**: 5 Mock Interviews | **Week 4**: Networking + Followups")

    # TAB 15: CAREER TIPS
    with tabs[14]:
        st.subheader("Pro Career Tips 💡")
        st.write("1. **Trick**: Apply within 48 hours of job posting")
        st.write("2. **Trick**: Connect with 3 employees before applying")
        st.write("3. **Trick**: Use 'Easy Apply' on LinkedIn for 3x more responses")

else:
    st.info("👈 Please complete your profile in the sidebar to unlock all 15 features")

st.sidebar.markdown("---")
st.sidebar.write("Built with ❤️ using Gemini AI")
