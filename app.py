import streamlit as st
import pandas as pd
import plotly.express as px
import pdfplumber
import docx
import google.generativeai as genai

st.set_page_config(page_title="AI Career Coach Pro", page_icon="🚀", layout="wide")

API_READY = False
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    API_READY = True
    st.sidebar.success("✅ Gemini Connected")
except:
    st.sidebar.error("❌ GOOGLE_API_KEY not found")

st.title("🚀 AI Career Coach Pro")

role = st.sidebar.text_input("🎯 Target Role", "Data Analyst")
exp = st.sidebar.selectbox("💼 Experience", ["Fresher", "1-2 Years"])

tabs = st.tabs(["❓ AI Interview", "📊 ATS Score"])

with tabs[0]:
    if not API_READY: st.error("⚠️ Add GOOGLE_API_KEY")
    elif st.button("Generate 10 Questions"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"10 interview questions for {role} with {exp}")
        st.write(res.text)

with tabs[1]:
    if not API_READY: st.error("⚠️ Add GOOGLE_API_KEY")
    elif st.button("Analyze"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Give ATS Score for {role}")
        st.write(res.text)
