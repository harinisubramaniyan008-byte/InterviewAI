import streamlit as st
import pandas as pd
import plotly.express as px
import pdfplumber
import docx
from groq import Groq

st.set_page_config(page_title="AI Career Coach Pro", page_icon="🚀", layout="wide")

# GROQ API KEY CHECK
API_READY = False
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
    API_READY = True
except:
    API_READY = False

st.markdown("""
<style>
.stApp { background-color: #ffffff; }
h1 { color: #1a365d!important; text-align: center; font-weight: 700; }
[data-testid="stSidebar"] { background-color: #f7fafc; }
.stTabs [aria-selected="true"] { background-color: #2b6cb0!important; color: white!important; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Career Coach Pro")

# SIDEBAR
st.sidebar.header("Your Profile")
if API_READY: st.sidebar.success("✅ Groq Connected")
else: st.sidebar.error("❌ GROQ_API_KEY not found")

location = st.sidebar.selectbox("📍 Location", ["Chennai", "Bangalore", "Hyderabad", "Remote", "Pune"])
role = st.sidebar.text_input("🎯 Target Role", "Data Analyst")
exp = st.sidebar.selectbox("💼 Experience", ["Fresher", "1-2 Years", "3-5 Years"])
uploaded_file = st.sidebar.file_uploader("📄 Upload Resume PDF/DOCX", type=["pdf", "docx"])

def read_resume(file):
    if file is None: return ""
    try:
        text = ""
        if file.type == "application/pdf":
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages: text += page.extract_text() or ""
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(file)
            for para in doc.paragraphs: text += para.text
        return text
    except: return ""

resume_text = read_resume(uploaded_file)

# 15 TABS
tabs = st.tabs([
    "📍 Overview", "🏢 Companies", "💰 Salary", "🎓 Internships", "❓ AI Interview",
    "📊 ATS Score", "🔔 Alerts", "📈 Skills Roadmap", "🏆 Code Practice",
    "📧 Email AI", "🌐 LinkedIn AI", "📝 Keywords", "🎤 Mock Interview", "📅 30-Day Plan", "💡 Pro Tips"
])

with tabs[0]:
    st.subheader("Dashboard Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Jobs Found", "127", "+12%")
    col2.metric("Market Demand", "HIGH 🔥")
    col3.metric("Your Match", "78%", "+5%")

with tabs[1]:
    st.subheader("Top Companies Hiring")
    st.dataframe(pd.DataFrame({'Company':['TCS','Zoho','Freshworks','Infosys','Wipro'],'Role':[role]*5,'Location':[location]*5,'Openings':[12,5,8,10,7]}),use_container_width=True)

with tabs[2]:
    st.subheader("Salary Predictor")
    col1, col2, col3 = st.columns(3)
    col1.metric("Fresher", "₹3.6 - ₹6 LPA")
    col2.metric("2 Yrs Exp", "₹8 - ₹12 LPA")
    col3.metric("5 Yrs Exp", "₹15 - ₹25 LPA")
    st.plotly_chart(px.bar(x=["Fresher", "2Y", "5Y"], y=[4.5, 10, 20], title="Salary Growth"), use_container_width=True)

with tabs[3]:
    st.subheader("Latest Internships")
    st.dataframe(pd.DataFrame({'Company':['Zoho','Google','Microsoft'],'Role':['Data Intern','AI Intern','Product Intern'],'Stipend':['₹25,000','₹80,000','₹70,000']}),use_container_width=True)

with tabs[4]: # AI
    st.subheader("AI Interview Questions")
    if not API_READY: st.error("⚠️ Add GROQ_API_KEY in Streamlit Settings > Secrets")
    elif st.button("Generate 10 Questions"):
        with st.spinner("Generating..."):
            chat = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":f"Generate 10 interview questions for {role} with {exp} experience in {location}"}])
            st.write(chat.choices[0].message.content)

with tabs[5]: # AI
    st.subheader("ATS Resume Score")
    if not uploaded_file: st.warning("👈 First upload your resume")
    elif not API_READY: st.error("⚠️ Add GROQ_API_KEY")
    elif st.button("Analyze Resume"):
        with st.spinner("Analyzing..."):
            chat = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":f"Analyze this resume for {role} role. Give ATS Score out of 100, 5 missing skills, and 3 improvement tips. Resume: {resume_text[:3000]}"}])
            st.write(chat.choices[0].message.content)

with tabs[6]: st.subheader("Job Alerts"); st.warning("⚠️ TCS Drive - Last 48 hours"); st.info("📧 3 new jobs matched"); st.success("🤝 2 referrals available")
with tabs[7]: st.subheader("90-Day Skills Roadmap"); st.progress(30); st.write("**Month 1**: SQL + Excel | **Month 2**: PowerBI + Python | **Month 3**: ML + Cloud")
with tabs[8]: st.subheader("Daily Coding Practice"); st.code("Q: Find Second Largest"); st.button("Show Solution") and st.code("def second_largest(arr):\n return sorted(set(arr))[-2]")

with tabs[9]: # AI
    st.subheader("AI Email Writer")
    if not API_READY: st.error("⚠️ Add GROQ_API_KEY")
    elif st.button("Generate Email"):
        chat = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":f"Write professional Referral Request email for {role} position"}])
        st.text_area("Email", chat.choices[0].message.content, height=200)

with tabs[10]: # AI
    st.subheader("LinkedIn Profile Optimizer")
    if not API_READY: st.error("⚠️ Add GROQ_API_KEY")
    elif st.button("Generate About Section"):
        chat = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":f"Write LinkedIn About section for {role} with {exp} experience"}])
        st.text_area("About", chat.choices[0].message.content, height=150)

with tabs[11]: st.subheader("Top 20 ATS Keywords"); st.write(", ".join(["Python","SQL","PowerBI","Tableau","ML","ETL","Pandas","NumPy","Statistics","Analytics"]))
with tabs[12]: # AI
    st.subheader("AI Mock Interview")
    if not API_READY: st.error("⚠️ Add GROQ_API_KEY")
    else:
        ans=st.text_area("Q: Tell me about yourself")
        if st.button("Get AI Feedback"):
            chat = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":f"Give feedback for this interview answer: {ans}. Score out of 10 and 2 tips."}])
            st.info(chat.choices[0].message.content)
with tabs[13]: st.subheader("30-Day Job Hunt Plan"); st.write("**Week 1**: Resume | **Week 2**: Apply 50 jobs | **Week 3**: Mock Interviews | **Week 4**: Networking")
with tabs[14]: st.subheader("Pro Career Tips"); st.write("1. Apply within 48 hours\n2. Connect with 3 employees\n3. Use Easy Apply\n4. Customize resume")
