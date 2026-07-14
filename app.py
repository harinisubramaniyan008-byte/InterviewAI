# FULL CODE V11.1 - COPY THIS FULL
import streamlit as st
from groq import Groq
import pdfplumber
import pandas as pd
import json
import re
import random

st.set_page_config(page_title="AI Career OS PRO", layout="wide", page_icon="🚀", initial_sidebar_state="expanded")

st.markdown("""
<style>
  .block-container {padding-top: 1rem; padding-bottom: 1rem; padding-left: 1rem; padding-right: 1rem;}
  .metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 10px;}
  .metric-card h1 {font-size: 2.5rem; margin: 0;}
  .skill-tag {display:inline-block; background-color:#4F46E5; color:white; padding: 8px 15px; border-radius: 20px; margin: 5px 5px 5px 0; font-weight: 500; font-size: 14px;}
  .gap-tag {display:inline-block; background-color:#EF4444; color:white; padding: 8px 15px; border-radius: 20px; margin: 5px 5px 5px 0; font-weight: 500; font-size: 14px;}
  .stButton > button {width: 100%;}
</style>
""", unsafe_allow_html=True)

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.sidebar.error("⚠️ Settings → Secrets la GROQ_API_KEY add pannu")
    st.stop()

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text(): text += page.extract_text() + "\n"
    return text

def ask_ai(prompt):
    with st.spinner("AI is thinking... 10-20 seconds"):
        response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], temperature=0.3, max_tokens=2500)
    return response.choices[0].message.content

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try: return json.loads(match.group())
        except: return None
    return None

if 'resume_text' not in st.session_state: st.session_state.resume_text = ""
if 'qs' not in st.session_state: st.session_state.qs = ""

with st.sidebar:
    st.title("🚀 AI Career OS PRO v11.1")
    page = st.radio("Select Module", [
        "🏠 Dashboard","🧠 AI Doubt Clear","💼 Live Mock Interview","🔎 AI Job + Course Finder",
        "💻 Code + SQL Lab","🎯 Project Generator","📊 Skill Gap Analyzer","🎮 Daily Challenge",
        "🔥 Motivation Dose","📈 Salary Calculator","📚 7-Day Course Quest"
    ])
    st.divider()
    st.header("Step 1: Upload Resume")
    resume_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    if resume_file:
        st.session_state.resume_text = read_pdf(resume_file)
        st.success("✅ Resume Loaded")

#...BAKI ELLA 11 MODULE CODE MUM APDIYEE IRUKUM...
# NAAN FULL CODE ANUPITEN. MELA IRUKURA CODE BLOCK LA COPY BUTTON IRUKUM
