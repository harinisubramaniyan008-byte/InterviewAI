import streamlit as st
from groq import Groq
import pdfplumber
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

st.set_page_config(page_title="AI Career Coach TECH PRO", layout="wide", page_icon="🚀")

# PRO CSS
st.markdown("""
<style>
.metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white; text-align: center;}
.big-card {background-color: #FFFFFF; padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Career Coach TECH PRO")
st.caption("AI-Powered Career Intelligence Dashboard | Built for 2026")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Please add GROQ_API_KEY in Streamlit Secrets")
    st.stop()

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

@st.cache_data(show_spinner="AI Analyzing... 30 seconds")
def get_pro_analysis(resume_text, location):
    prompt = f"""
    Return ONLY valid JSON. Be technical and data-driven.
    RESUME: {resume_text}
    LOCATION: {location}

    JSON format:
    {{
      "ats_score": 78,
      "ats_breakdown": {{"Keywords": 75, "Experience": 80, "Education": 90, "Skills": 70}},
      "skill_radar_you": {{"Python": 8, "SQL": 7, "PowerBI": 3, "ML": 4, "Excel": 9}},
      "skill_radar_job": {{"Python": 9, "SQL": 9, "PowerBI": 8, "ML": 7, "Excel": 8}},
      "companies": [{{"name": "Zoho", "openings": 23}}, {{"name": "TCS", "openings": 45}}, {{"name": "Freshworks", "openings": 12}}],
      "salary_roi": [{{"skill": "PowerBI", "salary_hike": "+22%"}}, {{"skill": "ML", "salary_hike": "+35%"}}],
      "resume_rewrite": ["Old: Worked on data", "New: Analyzed 10GB+ data using Python & SQL, improved reporting speed by 40%"],
      "competitor_rank": 23
    }}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=3000,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# SIDEBAR
with st.sidebar:
    st.header("Step 1: Upload Resume")
    resume_file = st.file_uploader("Upload PDF", type=["pdf"])
    st.header("Step 2: Target City")
    location = st.selectbox("", ["Chennai", "Bangalore", "Hyderabad", "Pune"])

# BUTTON
if resume_file:
    if st.button("🚀 Generate Tech Report", use_container_width=True, type="primary"):
        with st.spinner("AI is building your dashboard..."):
            resume_text = read_pdf(resume_file)
            try:
                data = get_pro_analysis(resume_text, location)
                st.session_state.data = data
                st.success("✅ Report Generated!")
            except Exception as e:
                st.error(f"AI Error: {e}. Please try again")

# IMPORTANT: ITHU DHAN FIX - DATA IRUNDA MATTUM KATU
if 'data' in st.session_state:
    data = st.session_state.data

    # TOP METRICS
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f'<div class="metric-card"><h3>ATS Score</h3><h1>{data["ats_score"]}/100</h1></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="metric-card"><h3>Market Rank</h3><h1>Top {data["competitor_rank"]}%</h1></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="metric-card"><h3>Companies</h3><h1>{len(data["companies"])} Hiring</h1></div>', unsafe_allow_html=True)

    st.write("")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Skill Analytics", "🏢 Market Data", "✍️ AI Tools", "📈 Salary ROI"])

    with tab1:
        st.subheader("Your Skills vs Job Market Demand")
        df_radar = pd.DataFrame({
            'Skill': list(data['skill_radar_you'].keys()),
            'You': list(data['skill_radar_you'].values()),
            'Job Demand': list(data['skill_radar_job'].values())
        })
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=df_radar['You'], theta=df_radar['Skill'], fill='toself', name='Your Skills'))
        fig.add_trace(go.Scatterpolar(r=df_radar['Job Demand'], theta=df_radar['Skill'], fill='toself', name='Job Demand'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), height=400, legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader(f"Hiring Trend in {location}")
        df_comp = pd.DataFrame(data['companies'])
        fig2 = px.bar(df_comp, x='name', y='openings', color='openings', title="Active Job Openings")
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.subheader("AI Resume Bullet Rewriter")
        st.write("**Before:**", data['resume_rewrite'][0])
        st.success("**After ATS Optimization:** " + data['resume_rewrite'][1])

    with tab4:
        st.subheader("Skill = Money. Learn this, earn more.")
        df_roi = pd.DataFrame(data['salary_roi'])
        st.dataframe(df_roi, use_container_width=True)

else:
    st.info("👈 Step 1: Upload resume in sidebar \n\n Step 2: Click 'Generate Tech Report'")
