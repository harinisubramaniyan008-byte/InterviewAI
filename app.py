import streamlit as st
import google.generativeai as genai

st.title("AI Career Coach Pro")

# Debug mode
st.write("Key iruka:", "GOOGLE_API_KEY" in st.secrets) 

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"]) # try/except eduthudu
model = genai.GenerativeModel('gemini-1.5-flash')
st.success("Key work aagudhu!")
