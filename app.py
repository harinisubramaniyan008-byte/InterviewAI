import streamlit as st
import pandas as pd
import plotly.express as px
import os
import pdfplumber
import docx
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key from GitHub Secrets
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="AI Career Coach Pro V2", page_icon="🚀", layout="wide")

# CSS for cards
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.2);
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Career Coach Pro V2")

# SIDEBAR
st.sidebar.header("Ungal Profile")
location = st.sidebar.selectbox("📍 Location Select Pannu", ["Chennai", "Coimbatore", "Bangalore", "Hyderabad", "Remote"])
role = st.sidebar.text_input("🎯 Target Role", "Data Analyst")
uploaded_file = st.sidebar.file_uploader("📄 Resume Upload pannu", type=["pdf", "docx"])

# Dummy Data - ipo kku manual data
companies_data = {
    'Company': ['TCS', 'Zoho', 'Freshworks', 'Infosys', 'Wipro'],
    'Location': ['Chennai', 'Chennai', 'Chennai', 'Chennai', 'Chennai'],
    'Role': ['Data Analyst', 'Data Analyst', 'Data Analyst', 'Data Analyst', 'Data Analyst'],
    'Openings': [12, 5, 8, 10, 7],
    'Salary_LPA': ['3.6 - 6', '6 - 10', '8 - 15', '4 - 7', '3.5 - 6.5']
}
companies_df = pd.DataFrame(companies_data)

internships_data = {
    'Company': ['Zoho', 'TCS', 'Freshworks'],
    'Location': ['Chennai', 'Chennai', 'Chennai'],
    'Role': ['Data Intern', 'AI Intern', 'Product Intern'],
    'Stipend': ['₹15,000', '₹20,000', '₹25,000'],
    'Last_Date': ['2026-04-30', '2026-05-15', '2026-05-01']
}
internships_df = pd.DataFrame(internships_data)

filtered_companies = companies_df[companies_df['Location'] == location]

if uploaded_file and role:
    tabs = st.tabs(["📍 Overview", "🏢 Companies", "💰 Salary", "🎓 Internships", "❓ Interview", "📊 Match %", "🔔 Alerts"])

    with tabs[0]:
        st.subheader("1. Location Smart Alert 📍")
        st.write(f"**{location}** la **{len(filtered_companies)}** companies iruku")
        st.dataframe(filtered_companies[['Company', 'Role', 'Openings']], use_container_width=True)

        st.subheader("2. Company Fit Score 🎯")
        st.progress(82)
        st.write("Zoho ku unga fit: **82%** - Python skill match aagudhu. Excel konjam improve pannanum")

    with tabs[1]:
        st.subheader("Top Companies in " + location)
        for i, row in filtered_companies.iterrows():
            st.success(f"**{row['Company']}** - {row['Role']} | {row['Openings']} Openings | Salary: {row['Salary_LPA']} LPA")

    with tabs[2]:
        st.subheader("Salary Predictor 💰")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="metric-card"><h3>Per Month</h3><h2>₹30K - ₹50K</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card"><h3>Per Year</h3><h2>₹3.6 - ₹6 LPA</h2></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card"><h3>2 Yrs Exp</h3><h2>₹8 LPA</h2></div>', unsafe_allow_html=True)

        fig = px.bar(x=["Fresher", "2 Yrs Exp", "5 Yrs Exp"], y=[4.5, 8, 15], title="Experience vs Salary Growth")
        st.plotly_chart(fig, use_container_width=True)

    with tabs[3]:
        st.subheader("Open Internships 🎓")
        st.dataframe(internships_df[internships_df['Location'] == location], use_container_width=True)

    with tabs[4]:
        st.subheader("Interview Questions ❓")
        if st.button("Generate Questions"):
            prompt = f"Generate 5 important interview questions for {role} role in {location} for fresher"
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.write(response.text)

    with tabs[5]:
        st.subheader("Resume to JD Match % 📊")
        st.progress(65)
        st.warning("Missing Skills: SQL, PowerBI. Idha add pannuna 85% varum")
        if st.button("AI Resume ah Improve pannu"):
            st.info("Gemini un resume ah analyze panni keyword add pannum")

    with tabs[6]:
        st.subheader("Job Alerts 🔔")
        st.warning("⚠️ TCS Data Analyst - Last 2 days to apply!")
        st.info("Daily 9AM ku pudhu 5 jobs varum")
        st.success("Referral: Infosys la unga college senior 2 per irukanga")

else:
    st.info("👈 Sidebar la Location, Role kuduthu Resume upload pannunga")
