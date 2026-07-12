import streamlit as st
import os # <--- idhu pudhusu
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import pdfplumber
from docx import Document
import mysql.connector

st.set_page_config(page_title="AI Career Coach Pro", layout="wide")

# --- Sidebar ---
st.sidebar.title("🎯 Target Role")
role = st.sidebar.text_input("Target Role", "Data Analyst")
experience = st.sidebar.selectbox("Experience", ["Fresher", "1-2 Years", "3-5 Years", "5+ Years"])

# --- KEY LOAD PANRA LOGIC - 2 VAZHI ---
api_key = None

# 1. Mudhala Secrets la iruka nu paakum
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

# 2. Secrets la illana Environment Variable la irundhu edukatum
if not api_key:
    api_key = os.environ.get("GOOGLE_API_KEY")

# --- GEMINI CONNECT ---
if api_key:
    genai.configure(api_key=api_key)
    st.sidebar.success("✅ Gemini Connected")
else:
    st.sidebar.error("❌ GOOGLE_API_KEY not found")
    st.warning("⚠️ Add GOOGLE_API_KEY in Settings > Advanced settings > Environment variables")
    st.stop()

st.title("🚀 AI Career Coach Pro")
tab1, tab2 = st.tabs(["❓ AI Interview", "📊 ATS Score"])

with tab1:
    st.header("AI Mock Interview")
    if st.button("Start Interview"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"You are an HR. Ask 3 interview questions for a {role} with {experience} experience."
        response = model.generate_content(prompt)
        st.write(response.text)

with tab2:
    st.header("ATS Resume Score")
    uploaded_file = st.file_uploader("Upload Resume PDF/DOCX", type=["pdf","docx"])
    if uploaded_file:
        st.success("File uploaded! ATS feature coming soon.")
