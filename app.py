import streamlit as st
from groq import Groq

# API Key
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def analyze_resume(resume_text, jd_text):
    prompt = f"""
    You are AI Career Coach. Analyze this resume vs JD.
    Resume: {resume_text}
    JD: {jd_text}
    Give score out of 100 and feedback.
    """

    # ITHA MAATHU DA 👇
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # mela irundhadhu: llama-3.1-70b-versatile
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=2000
    )
    return response.choices[0].message.content
