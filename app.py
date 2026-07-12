import streamlit as st
import pdfplumber
import docx
from groq import Groq
import json
import time

st.set_page_config(page_title="AI Career Coach Pro", page_icon="🚀", layout="wide")

# CSS for animation and cards
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
   .tab-content {
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def extract_text(uploaded_file):
    text = ""
    if uploaded_file.name.endswith(".pdf"):
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                if page.extract_text(): text += page.extract_text() + "\n"
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs: text += para.text + "\n"
    else: text = uploaded_file.read().decode("utf-8")
    return text

st.title("🚀 AI Career Coach Pro")
st.caption("Upload pannunga... AI ungaluku offer letter varaikum guide panum")

uploaded_file = st.file_uploader("📤 Drag & Drop Your Resume Here", type=["pdf", "docx", "txt"])
job_desc = st.text_area("🎯 Target Job Description", height=100, placeholder="Ex: Data Analyst role at Google...")

if uploaded_file:
    resume_text = extract_text(uploaded_file)
    st.success(f"✅ {uploaded_file.name} Loaded Successfully!")

    if st.button("✨ Generate AI Analysis", type="primary", use_container_width=True):

        # ANIMATION 1: Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        for i in range(100):
            status_text.text(f"AI is scanning your resume... {i+1}%")
            progress_bar.progress(i + 1)
            time.sleep(0.05)
        status_text.text("AI Analysis Complete! 🎉")
        time.sleep(0.5)
        st.balloons() # ANIMATION 2: Balloons

        with st.spinner("Finalizing Report..."):
            prompt = f"""
            You are a world-class HR. Analyze this resume.
            Resume: {resume_text}
            Target Job: {job_desc}
            Return ONLY valid JSON:
            {{"overall_score": "85/100", "ats_score": "70/100", "summary": "...", "keyword_gaps": [".."], "strengths": [".."], "weaknesses": [".."], "suggestions": [".."], "hr_questions": [".."]}}
            """
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            st.session_state['data'] = json.loads(response.choices[0].message.content)

    if 'data' in st.session_state:
        data = st.session_state['data']

        tab1, tab2, tab3 = st.tabs(["📊 Analysis", "🎯 ATS & Skills", "❓ Mock Interview"])

        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1: st.markdown(f'<div class="metric-card"><h2>{data.get("overall_score")}</h2><p>Overall Score</p></div>', unsafe_allow_html=True)
            with col2: st.markdown(f'<div class="metric-card"><h2>{data.get("ats_score")}</h2><p>ATS Match</p></div>', unsafe_allow_html=True)
            with col3: st.metric("Keyword Gaps", len(data.get("keyword_gaps", [])))

            st.subheader("📝 AI Summary")
            st.info(data.get("summary"))

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("💪 Strengths")
                for s in data.get("strengths", []): st.success(f"✅ {s}")
            with col2:
                st.subheader("📉 Improve Areas")
                for w in data.get("weaknesses", []): st.warning(f"⚠️ {w}")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🎯 Missing Keywords for ATS")
            for gap in data.get("keyword_gaps", []):
                st.error(f"Add this keyword: **{gap}**")
            st.subheader("💡 Suggestions to Improve")
            for sug in data.get("suggestions", []): st.write(f"- {sug}")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("❓ AI Mock HR Interview")
            for i, q in enumerate(data.get("hr_questions", []), 1):
                with st.expander(f"Q{i}: {q}"):
                    st.text_area("Type your answer:", key=f"ans{i}")
                    st.button("Get AI Feedback", key=f"fb{i}")
            st.markdown('</div>', unsafe_allow_html=True)
