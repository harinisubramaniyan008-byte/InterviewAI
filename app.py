import streamlit as st
import pdfplumber
import docx
from groq import Groq
import json

st.set_page_config(page_title="AI Resume + Interview", page_icon="📄", layout="wide")
st.title("📄 AI Resume Score + HR Interview App")
st.write("Resume ah upload pannu. AI unaku Score, Feedback, Interview Questions ellam kudukum.")

# Groq client - Secrets la irundhu key varum
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

uploaded_file = st.file_uploader("📤 Upload your Resume", type=["pdf", "docx", "txt"])

if uploaded_file:
    resume_text = extract_text(uploaded_file)
    st.success("Resume Uploaded Successfully!")

    with st.expander("👀 Extracted Resume Text"):
        st.text_area("", resume_text, height=250)

    if st.button("🚀 Get AI Resume Score & Feedback", use_container_width=True):
        with st.spinner("AI is analyzing your resume... 10 seconds"):
            prompt = f"""
            You are an expert HR and Career Coach. Analyze this resume carefully.

            Resume:
            {resume_text}

            Give output ONLY in this JSON format:
            {{
              "score": "85/100",
              "summary": "2 line overall summary",
              "strengths": ["strength 1", "strength 2", "strength 3"],
              "weaknesses": ["weakness 1", "weakness 2", "weakness 3"],
              "suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"],
              "hr_questions": ["Q1", "Q2", "Q3", "Q4", "Q5"]
            }}
            """

            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", # pudhu model
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2000
                )

                result = response.choices[0].message.content

                # JSON ah clean panni kaatanum
                try:
                    data = json.loads(result)
                except:
                    data = {"raw": result}

                st.subheader("🎯 AI Resume Score")
                st.metric("Overall Score", data.get("score", "N/A"))

                st.subheader("📝 Summary")
                st.write(data.get("summary", ""))

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("✅ Strengths")
                    for s in data.get("strengths", []):
                        st.write(f"- {s}")
                with col2:
                    st.subheader("⚠️ Areas to Improve")
                    for w in data.get("weaknesses", []):
                        st.write(f"- {w}")

                st.subheader("💡 Suggestions")
                for sug in data.get("suggestions", []):
                    st.write(f"- {sug}")

                st.subheader("❓ HR Interview Questions for You")
                for i, q in enumerate(data.get("hr_questions", []), 1):
                    st.write(f"{i}. {q}")

            except Exception as e:
                st.error(f"Error: {e}")
