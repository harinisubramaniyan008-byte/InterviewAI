import streamlit as st
import pandas as pd
import plotly.express as px
import pdfplumber
import docx
import google.generativeai as genai

st.set_page_config(page_title="AI Career Coach Pro", page_icon="🚀", layout="wide")

# DEBUG: API KEY CHECK
API_READY = False
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    API_READY = True
    API_STATUS = "✅ Connected"
except KeyError:
    API_STATUS = "❌ GOOGLE_API_KEY not found in Secrets"
except Exception as e:
    API_STATUS = f"❌ Error: {e}"

# CLEAN THEME
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
st.sidebar.write(f"**API Status:** {API_STATUS}") # IDHU IMPORTANT

location = st.sidebar.selectbox("📍 Location", ["Chennai", "Bangalore", "Hyderabad", "Remote", "Pune"])
role = st.sidebar.text_input("🎯 Target Role", "Data Analyst")
exp = st.sidebar.selectbox("💼 Experience", ["Fresher", "1-2 Years", "3-5 Years"])
uploaded_file = st.sidebar.file_uploader("📄 Upload Resume PDF/DOCX", type=["pdf", "docx"])

# FUNCTION: READ RESUME
def read_resume(file):
    if file is None: return ""
    try:
        text = ""
        if file.type == "application/pdf":
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(file)
            for para in doc.paragraphs:
                text += para.text
        return text
    except:
        return ""

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
    st.plotly_chart(px.bar(x=["Fresher", "2Y", "5Y"], y=[4.5, 10, 20], title="Salary Growth"), use_container_width=True)

with tabs[3]:
    st.subheader("Latest Internships")
    st.dataframe(pd.DataFrame({
        'Company':['Zoho','Google','Microsoft'],
        'Role':['Data Intern','AI Intern','Product Intern'],
        'Stipend':['₹25,000','₹80,000','₹70,000']
    }), use_container_width=True)

with tabs[4]:
    st.subheader("AI Interview Questions")
    if not API_READY:
        st.error("⚠️ Add GOOGLE_API_KEY in Streamlit Settings > Secrets and Reboot")
    else:
        if st.button("Generate 10 Questions"):
            with st.spinner("Generating..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Generate 10 interview questions for {role} with {exp} experience")
                st.write(response.text)

with tabs[5]:
    st.subheader("ATS Resume Score")
    if not uploaded_file:
        st.warning("👈 First upload your resume in sidebar")
    elif not API_READY:
        st.error("⚠️ Add GOOGLE_API_KEY in Streamlit Settings > Secrets")
    else:
        if st.button("Analyze Resume"):
            with st.spinner("Analyzing..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Analyze this resume for {role} role. Give ATS Score out of 100, 5 missing skills, and 3 improvement tips. Resume: {resume_text[:3000]}"
                st.write(model.generate_content(prompt).text)

with tabs[6]:
    st.subheader("Job Alerts")
    st.warning("⚠️ TCS Drive - Last 48 hours to apply!")
    st.info("📧 3 new jobs matched your profile today")
    st.success("🤝 2 referrals available in your network")

with tabs[7]:
    st.subheader("90-Day Skills Roadmap")
    st.progress(30)
    st.write("**Month 1**: SQL + Excel Advanced")
    st.write("**Month 2**: PowerBI + Python")
    st.write("**Month 3**: ML + Cloud Projects")

with tabs[8]:
    st.subheader("Daily Coding Practice")
    st.code("Q: Find Second Largest Element in Array")
    if st.button("Show Solution"):
        st.code("def second_largest(arr):\n return sorted(set(arr))[-2]")

with tabs[9]:
    st.subheader("AI Email Writer")
    if not API_READY:
        st.error("⚠️ Add GOOGLE_API_KEY in Streamlit Settings > Secrets")
    else:
        email_type = st.selectbox("Email Type", ["Referral Request", "Follow Up", "Thank You"])
        if st.button("Generate Email"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            st.text_area("Generated Email", model.generate_content(f"Write professional {email_type} email for {role} position").text, height=200)

with tabs[10]:
    st.subheader("LinkedIn Profile Optimizer")
    if not API_READY:
        st.error("⚠️ Add GOOGLE_API_KEY in Streamlit Settings > Secrets")
    else:
        if st.button("Generate About Section"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            st.text_area("About", model.generate_content(f"Write LinkedIn About section for {role} with {exp} experience").text, height=150)

with tabs[11]:
    st.subheader("Top 20 ATS Keywords")
    st.write(", ".join(["Python","SQL","PowerBI","Tableau","Machine Learning","Data Visualization","ETL","Pandas","NumPy","Statistics","Analytics","Dashboard","Big Data","Cloud","API","Excel","Communication","Problem Solving","Business Analysis","Reporting"]))

with tabs[12]:
    st.subheader("AI Mock Interview")
    if not API_READY:
        st.error("⚠️ Add GOOGLE_API_KEY in Streamlit Settings > Secrets")
    else:
        answer = st.text_area("Q: Tell me about yourself for a Data Analyst role")
        if st.button("Get AI Feedback"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            st.info(model.generate_content(f"Give feedback for this interview answer: {answer}. Score out of 10 and 2 improvement tips.").text)

with tabs[13]:
    st.subheader("30-Day Job Hunt Plan")
    st.write("**Week 1**: Update Resume + LinkedIn Profile")
    st.write("**Week 2**: Apply to 50 jobs daily")
    st.write("**Week 3**: 5 Mock Interviews + Skill Practice")
    st.write("**Week 4**: Networking + Followups")

with tabs[14]:
    st.subheader("Pro Career Tips")
    st.write("1. Apply within 48 hours of job posting = 3x more replies")
    st.write("2. Connect with 3 employees before applying")
    st.write("3. Use 'Easy Apply' on LinkedIn for faster responses")
    st.write("4. Customize resume for each job with keywords")
