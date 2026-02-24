import streamlit as st
import requests
import io, re, os
from pathlib import Path

# 1. Page Config
st.set_page_config(page_title="Pareto Meeting Summarizer", page_icon="📊", layout="centered")

# 2. Backend URL (Localhost for now)
# Change this line in app.py
BACKEND_URL = os.environ.get("BACKEND_URL", "https://pareto-principle-summarizer-backend.onrender.com")

# 3. CSS Styling
st.markdown("""
<style>
#MainMenu {visibility:hidden;} footer {visibility:hidden;}
.stApp {background:#F8FAFC;}
.hero {background:linear-gradient(135deg,#1E3A8A,#2563EB);color:white;padding:2.5rem 2rem;
        border-radius:16px;margin-bottom:2rem;text-align:center;box-shadow:0 8px 32px rgba(30,58,138,.18);}
.hero h1 {font-size:2.1rem;font-weight:800;margin:0 0 .3rem; color: white !important;}
.hero p  {font-size:1rem;opacity:.88;margin:0; color: white !important;}
.badge   {display:inline-block;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.35);
          border-radius:999px;padding:.2rem .85rem;font-size:.78rem;font-weight:600;
          letter-spacing:.5px;margin-bottom:.9rem;color:#BFDBFE;text-transform:uppercase;}
.summary-box {background:linear-gradient(135deg,#F0FDF4,#ECFDF5);border:2px solid #10B981;
              border-radius:14px;padding:1.8rem 2rem;margin-top:1.5rem;
              box-shadow:0 4px 20px rgba(16,185,129,.10);}
.summary-title {font-size:1.05rem;font-weight:800;color:#065F46;margin-bottom:1rem;
                border-bottom:1px solid #A7F3D0;padding-bottom:.7rem;}
.summary-content {font-size:.97rem;color:#1E293B;line-height:1.75;white-space:pre-wrap;}
.stButton>button {background:linear-gradient(135deg,#1E3A8A,#2563EB) !important;color:white !important;font-weight:700;
                  border:none;border-radius:10px;padding:.75rem 2rem;width:100%;}
</style>
""", unsafe_allow_html=True)

# 4. Hero Section
st.markdown("""
<div class="hero">
  <div class="badge">Pareto Principle · 80/20 Rule</div>
  <h1>Pareto Meeting Summarizer</h1>
  <p>Transform long transcripts into the critical 20% that delivers 90% of the context.</p>
</div>
""", unsafe_allow_html=True)

# 5. Helper Functions
def summarize_via_backend(transcript):
    try:
        # We call the /summarize endpoint on your FastAPI server
        response = requests.post(f"{BACKEND_URL}/summarize", json={"text": transcript})
        if response.status_code == 200:
            return response.json()["summary"], None
        return None, response.json().get("detail", "Backend Error")
    except Exception as e:
        return None, f"Could not connect to Backend: {e}"

# 6. UI Input Logic
st.markdown('<div style="background:#fff;border-radius:14px;padding:1.8rem 2rem;box-shadow:0 2px 16px rgba(30,58,138,.07);border:1px solid #E2E8F0;margin-bottom:1.5rem">', unsafe_allow_html=True)
st.markdown('<div style="font-size:1rem;font-weight:700;color:#1E3A8A;margin-bottom:.75rem">Transcript Input</div>', unsafe_allow_html=True)

transcript_text = st.text_area("Paste transcript", placeholder="Paste your meeting transcript here...", height=300, label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# 7. Action Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    clicked = st.button("Summarize", use_container_width=True)

# 8. Execution
if clicked:
    if not transcript_text.strip():
        st.warning("Please paste a transcript first.")
    else:
        with st.spinner("FastAPI is processing with Gemini AI..."):
            summary, error = summarize_via_backend(transcript_text)
            if error:
                st.error(error)
                st.info("Make sure your FastAPI backend (main.py) is running on port 8000!")
            else:
                st.markdown(f"""
                <div class="summary-box">
                  <div class="summary-title">Executive Summary — Key Takeaways</div>
                  <div class="summary-content">{summary}</div>

                </div>""", unsafe_allow_html=True)
