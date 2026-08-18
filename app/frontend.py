import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Dr. Panda 2.0 AI Medical Assistant", layout="wide")

# Custom CSS for Dr. Panda Character Theme & Cards
st.markdown("""
<style>
  .dr-panda-banner {
    background-color: #0b2545;
    color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 15px;
    border-left: 6px solid #00a896;
  }
  .dr-panda-title {
    font-size: 22pt;
    font-weight: 700;
    margin-bottom: 4px;
    text-transform: uppercase;
  }
  .dr-panda-subtitle {
    font-size: 11pt;
    color: #cbd5e1;
  }
  .disclaimer-box {
    background-color: #fff7ed;
    border: 1.5px solid #fdba74;
    color: #9a3412;
    padding: 12px 16px;
    border-radius: 6px;
    margin-bottom: 20px;
    font-size: 9pt;
    font-weight: 600;
  }
  .card-emergency {
    background-color: #fef2f2;
    border-left: 4px solid #ef4444;
    padding: 14px;
    border-radius: 4px;
    margin-top: 10px;
  }
  .card-moderate {
    background-color: #fffbebf;
    border-left: 4px solid #f59e0b;
    padding: 14px;
    border-radius: 4px;
    margin-top: 10px;
  }
  .card-low {
    background-color: #f0fdf4;
    border-left: 4px solid #22c55e;
    padding: 14px;
    border-radius: 4px;
    margin-top: 10px;
  }
</style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown("""
<div class="dr-panda-banner">
  <div class="dr-panda-title">Dr. Panda 2.0 AI Medical Intelligence Platform</div>
  <div class="dr-panda-subtitle">Interactive Panda Doctor Chatbot | Symptom Screening & Medical Lab Report Reader</div>
</div>
""", unsafe_allow_html=True)

# AI Disclaimer Exclamation Box
st.markdown("""
<div class="disclaimer-box">
  EXCLAMATION DISCLAIMER: Dr. Panda 2.0 is an AI medical screening assistant designed strictly for suggestive and educational purposes. It is not responsible for medical outcomes, does not substitute professional clinical diagnosis, and cannot issue official prescriptions. In case of emergency, contact local medical emergency services immediately.
</div>
""", unsafe_allow_html=True)

# Initialize Session State Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello there! I am Dr. Panda, your AI healthcare assistant. How can I help you today? You can describe your symptoms or upload a medical report for insights!"}
    ]

tab1, tab2 = st.tabs(["Interactive Chat with Dr. Panda", "Upload & Read Medical Reports"])

# Tab 1: Interactive Chatbot
with tab1:
    col_chat, col_info = st.columns([2, 1])
    
    with col_chat:
        st.subheader("Symptom Chat Room")
        
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        user_input = st.chat_input("Describe your symptoms to Dr. Panda...")
        
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
                
            from app.panda_engine import PandaDoctorEngine
            engine = PandaDoctorEngine()
            result = engine.process_query(user_input)
            
            reply_text = f"{result['panda_reply']}\n\nCondition Screened: {result['condition']}\nUrgency Rating: {result['urgency_level']}\nRecommended Action: {result['action_recommendation']}\nHome Care Advice: {result['home_care_advice']}"
            
            st.session_state.messages.append({"role": "assistant", "content": reply_text})
            with st.chat_message("assistant"):
                st.write(reply_text)
                
    with col_info:
        st.subheader("Dr. Panda Triage Guide")
        st.info("Dr. Panda categorizes health requirements into three primary ratings:")
        st.markdown("**1. Emergency Priority**: Seek Immediate Emergency Medical Care")
        st.markdown("**2. Moderate Priority**: Schedule a Doctor Appointment within 24 Hours")
        st.markdown("**3. Low Priority**: Home Care, Rest, Hydration, and Monitoring")

# Tab 2: Upload & Read Medical Reports
with tab2:
    st.subheader("Medical Report Reader & Lab Insight Generator")
    st.write("Upload a digital lab report file (TXT or CSV format) for Dr. Panda 2.0 to parse, detect health markers, and calculate urgency requirements.")
    
    uploaded_file = st.file_uploader("Choose a Medical Report file", type=["txt", "csv"])
    
    if uploaded_file is not None:
        file_text = uploaded_file.read().decode("utf-8", errors="ignore")
        
        with st.spinner("Dr. Panda is reading and analyzing your report markers..."):
            from app.report_analyzer import MedicalReportAnalyzer
            analyzer = MedicalReportAnalyzer()
            res = analyzer.analyze_report_text(file_text)
            
            st.success("Report analysis complete.")
            
            st.markdown("### Executive Health Summary")
            st.write(res["overall_health_insight"])
            
            c1, c2 = st.columns(2)
            c1.metric("Urgency Priority Rating", res["urgency_rating"])
            c2.metric("Hospital Visit Required", "Yes - Immediate" if res["hospital_visit_required"] else "No - Standard Care")
            
            if res["detected_markers"]:
                st.markdown("### Detected Lab Biomarkers")
                df_markers = pd.DataFrame(res["detected_markers"])
                st.table(df_markers)
