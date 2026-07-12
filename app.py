import streamlit as st
import pandas as pd
import plotly.express as px
import pdfplumber
import docx
import google.generativeai as genai

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    API_READY = True
except:
    API_READY = False

st.set_page_config(page_title="AI Career Coach Pro", page_icon="🚀", layout="wide")
st.markdown("""<style>.stApp{background-color:#ffffff;}h1{color:#1a365d!important;text-align:center;font-weight:700;}[data-testid="stSidebar"]{background-color:#f7fafc;}.stTabs [aria-selected="true"]{background-color:#2b6cb0!important;color:white!important;}</style>""", unsafe_allow_html=True)

st.title("🚀 AI Career Coach Pro")

st.sidebar.header("Your Profile")
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
tabs = st.tabs(["📍 Overview","🏢 Companies","💰 Salary","🎓 Internships","❓ AI Interview","📊 ATS Score","🔔 Alerts","📈 Skills Roadmap","🏆 Code Practice","📧 Email AI","🌐 LinkedIn AI","📝 Keywords","🎤 Mock Interview","📅 30-Day Plan","💡 Pro Tips"])

with tabs[0]:
    st.subheader("Dashboard Overview")
    col1,col2,col3=st.columns(3)
    col1.metric("Jobs Found","127","+12%");col2.metric("Market Demand","HIGH 🔥");col3.metric("Your Match","78%","+5%")

with tabs[1]:
    st.subheader("Top Companies Hiring")
    st.dataframe(pd.DataFrame({'Company':['TCS','Zoho','Freshworks','Infosys','Wipro'],'Role':[role]*5,'Location':[location]*5,'Openings':[12,5,8,10,7]}),use_container_width=True)

with tabs[2]:
    st.subheader("Salary Predictor")
    col1,col2,col3=st.columns(3)
    col1.metric("Fresher","₹3.6 - ₹6 LPA");col2.metric("2 Yrs Exp","₹8 - ₹12 LPA");col3.metric("5 Yrs Exp","₹15 - ₹25 LPA")
    st.plotly_chart(px.bar(x=["Fresher","2Y","5Y"],y=[4.5,10,20],title="Salary Growth"),use_container_width=True)

with tabs[3]:
    st.subheader("Latest Internships")
    st.dataframe(pd.DataFrame({'Company':['Zoho','Google','Microsoft'],'Role':['Data Intern','AI Intern','Product Intern'],'Stipend':['₹25,000','₹80,000','₹70,000'],'Deadline':['30-Apr-2026','15-May-2026','01-Jun-2026']}),use_container_width=True)

with tabs[4]:
    st.subheader("AI Interview Questions")
    if not API_READY: st.error("⚠️ Add GOOGLE_API_KEY in Streamlit Settings > Secrets")
    elif st.button("Generate 10 Questions"):
        with st.spinner("Generating..."):
            st.write(genai.GenerativeModel('gemini-1.5-flash').generate_content(f"10 interview questions for {role} with {exp}").text)

with tabs[5]:
    st.subheader("ATS Resume Score")
    if not uploaded_file: st.warning("👈 First upload your resume")
    elif not API_READY: st.error("⚠️ Add GOOGLE_API_KEY in Secrets")
    elif st.button("Analyze Resume"):
        with st.spinner("Analyzing..."):
            st.write(genai.GenerativeModel('gemini-1.5-flash').generate_content(f"Analyze resume for {role}. Give Score, missing skills. Resume:{resume_text[:3000]}").text)

with tabs[6]:
    st.subheader("Job Alerts")
    st.warning("⚠️ TCS Drive - Last 48 hours");st.info("📧 3 new jobs matched");st.success("🤝 2 referrals available")

with tabs[7]:
    st.subheader("90-Day Skills Roadmap")
    st.progress(30);st.write("**Month 1**: SQL + Excel | **Month 2**: PowerBI + Python | **Month 3**: ML + Cloud")

with tabs[8]:
    st.subheader("Daily Coding Practice")
    st.code("Q: Find Second Largest Element in Array");st.button("Show Solution") and st.code("def second_largest(arr):\n return sorted(set(arr))[-2]")

with tabs[9]:
    st.subheader("AI Email Writer")
    if not API_READY: st.error("⚠️ Add GOOGLE_API_KEY")
    elif st.button("Generate Email"):
        st.text_area("Email",genai.GenerativeModel('gemini-1.5-flash').generate_content(f"Referral email for {role}").text,height=200)

with tabs[10]:
    st.subheader("LinkedIn Profile Optimizer")
    if not API_READY: st.error("⚠️ Add GOOGLE_API_KEY")
    elif st.button("Generate About"):
        st.text_area("About",genai.GenerativeModel('gemini-1.5-flash').generate_content(f"LinkedIn About for {role}").text,height=150)

with tabs[11]:
    st.subheader("Top 20 ATS Keywords")
    st.write(", ".join(["Python","SQL","PowerBI","Tableau","ML","ETL","Pandas","NumPy","Statistics","Analytics","Dashboard","Big Data","Cloud","API","Excel","Communication"]))

with tabs[12]:
    st.subheader("AI Mock Interview")
    if not API_READY: st.error("⚠️ Add GOOGLE_API_KEY")
    else:
        ans=st.text_area("Q: Tell me about yourself")
        if st.button("Get AI Feedback"): st.info(genai.GenerativeModel('gemini-1.5-flash').generate_content(f"Feedback:{ans}").text)

with tabs[13]:
    st.subheader("30-Day Job Hunt Plan")
    st.write("**Week 1**: Resume + LinkedIn | **Week 2**: Apply 50 jobs | **Week 3**: 5 Mock Interviews | **Week 4**: Networking")

with tabs[14]:
    st.subheader("Pro Career Tips")
    st.write("1. Apply within 48 hours\n2. Connect with 3 employees\n3. Use Easy Apply\n4. Customize resume")
