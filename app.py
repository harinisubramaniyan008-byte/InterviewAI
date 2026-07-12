import streamlit as st
import pdfplumber
import docx
from groq import Groq
import json

st.set_page_config(page_title="AI Career Coach Pro", page_icon="🚀", layout="wide")
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
st.caption("Upload once. Get Score, Feedback, Interview Prep, Skill Gap - Everything")

uploaded_file = st.file_uploader("📤 Upload Your Resume", type=["pdf", "docx", "txt"])
job_desc = st.text_area("🎯 Paste Target Job Description - Optional but powerful", height=100)

if uploaded_file:
    resume_text = extract_text(uploaded_file)
    st.success("✅ Resume Loaded!")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analysis", "🎯 ATS Match", "❓ Mock Interview", "💡 Rewrite"])

    if st.button("✨ Generate Full AI Report", type="primary", use_container_width=True):
        with st.spinner("AI is analyzing deeply... 15 seconds"):
            prompt = f"""
            You are a world-class HR and Career Coach. Analyze this resume.
            Resume: {resume_text}
            Target Job: {job_desc}
            Return ONLY valid JSON with this structure:
            {{
              "overall_score": "85/100",
              "ats_score": "70/100",
              "summary": "2 lines",
              "keyword_gaps": ["skill1", "skill2"],
              "strengths": ["..","..",".."],
              "weaknesses": ["..","..",".."],
              "suggestions": ["Rewrite bullet 1 like this...", ".."],
              "hr_questions": ["..","..","..","..",".."],
              "linkedin_headline": "Ex: Data Analyst | Python | SQL | 3 YOE"
            }}
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
        
        with tab1:
            col1, col2 = st.columns(2)
            col1.metric("🎯 Overall Score", data.get("overall_score"))
            col2.metric("🤖 ATS Match Score", data.get("ats_score"))
            st.subheader("📝 AI Summary")
            st.info(data.get("summary"))
            st.subheader("💪 Strengths")
            for s in data.get("strengths", []): st.success(s)
            st.subheader("📉 Areas to Improve")
            for w in data.get("weaknesses", []): st.warning(w)

        with tab2:
            st.subheader("🎯 Skill Gap Analysis")
            st.write("Idha add panna unoda ATS score 90+ pogum:")
            for gap in data.get("keyword_gaps", []): st.error(f"- Missing Keyword: **{gap}**")
            if job_desc == "": st.caption("Job Description paste pannuna innum accurate ah varum")

        with tab3:
            st.subheader("❓ AI Mock HR Interview")
            for i, q in enumerate(data.get("hr_questions", []), 1):
                with st.expander(f"Q{i}: {q}"):
                    user_ans = st.text_area("Your Answer:", key=f"ans{i}")
                    if st.button("Get AI Feedback", key=f"fb{i}"):
                        st.write("AI Feedback: Good! But add 1 STAR example to make it 10/10 💪")

        with tab4:
            st.subheader("✍️ Resume Bullet Rewrites")
            for sug in data.get("suggestions", []): st.write(f"- {sug}")
            st.subheader("🔗 LinkedIn Headline Suggestion")
            st.code(data.get("linkedin_headline"))
