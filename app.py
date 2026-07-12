import streamlit as st
import pdfplumber
import docx
from groq import Groq
import json
import base64
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

st.set_page_config(page_title="AI Resume Pro", page_icon="🚀", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def extract_text(uploaded_file):
    text = ""
    if uploaded_file.name.endswith(".pdf"):
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        text = uploaded_file.read().decode("utf-8")
    return text

def create_pdf_report(data, name):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, y, "AI Resume Analysis Report")
    y -= 40
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Candidate: {name}")
    y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Overall Score: {data.get('score')}")
    y -= 30

    for section in ["summary", "strengths", "weaknesses", "suggestions", "hr_questions"]:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, section.upper())
        y -= 20
        c.setFont("Helvetica", 10)
        items = data.get(section, [])
        if isinstance(items, list):
            for item in items:
                c.drawString(60, y, f"- {item}")
                y -= 15
        else:
            c.drawString(60, y, f"- {items}")
            y -= 15
        y -= 10

    c.save()
    buffer.seek(0)
    return buffer

st.title("🚀 AI Resume Pro - Score, Feedback, Interview & PDF")
uploaded_file = st.file_uploader("📤 Upload Resume", type=["pdf", "docx", "txt"])

if uploaded_file:
    resume_text = extract_text(uploaded_file)
    st.success("✅ Resume Uploaded Successfully!")

    name = uploaded_file.name.split(".")[0]

    if st.button("✨ Generate AI Analysis", use_container_width=True, type="primary"):
        with st.spinner("AI is thinking..."):
            prompt = f"""
            You are an expert HR. Analyze this resume and return ONLY valid JSON.
            Resume: {resume_text}
            JSON Format:
            {{"score": "85/100", "summary": "...", "strengths": [".."], "weaknesses": [".."], "suggestions": [".."], "hr_questions": ["..","..","..","..",".."]}}
            """
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    response_format={"type": "json_object"} # idhu dhan mukkiyam
                )
                data = json.loads(response.choices[0].message.content)
                st.session_state['data'] = data
                st.session_state['name'] = name
            except Exception as e:
                st.error(f"Error: {e}")

    if 'data' in st.session_state:
        data = st.session_state['data']

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 Overall Score", data.get("score"))
        with col2:
            st.metric("✅ Strengths Count", len(data.get("strengths", [])))
        with col3:
            st.metric("⚠️ Improve Areas", len(data.get("weaknesses", [])))

        st.subheader("📝 AI Summary")
        st.info(data.get("summary"))

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("💪 Strengths")
            for s in data.get("strengths", []): st.success(f"- {s}")

            st.subheader("💡 Suggestions")
            for sug in data.get("suggestions", []): st.write(f"- {sug}")

        with col2:
            st.subheader("📉 Areas to Improve")
            for w in data.get("weaknesses", []): st.warning(f"- {w}")

            st.subheader("❓ HR Interview Questions")
            for i, q in enumerate(data.get("hr_questions", []), 1): st.write(f"{i}. {q}")

        st.markdown("---")
        pdf_buffer = create_pdf_report(data, st.session_state['name'])
        st.download_button(
            label="📥 Download Report as PDF",
            data=pdf_buffer,
            file_name=f"Resume_Report_{name}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
