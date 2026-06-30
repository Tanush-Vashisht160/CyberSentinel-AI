import os
import json
import streamlit as st

from analyzer.rule_engine import detect_rules
from analyzer.risk_calculator import calculate_risk
from analyzer.explanation_engine import get_explanations
from ai.gemini_client import analyze_prompt
from analyzer.logger import save_log
from analyzer.report_generator import generate_report

# ---------------- UI CONFIG & PREMIUM THEME ----------------
st.set_page_config(page_title="CyberSentinel AI", layout="wide", initial_sidebar_state="expanded")

# High-contrast premium dark theme with custom gradient matching your color palette accents
st.markdown("""
    <style>
    /* target the main container background and top status bars */
    .stApp, header[data-testid="stHeader"] {
        background: linear-gradient(145deg, #1b3a4b 0%, #272640 50%, #312244 100%) !important;
    }
    
    /* Remove default white border line at the very top of Streamlit */
    div[data-testid="stDecoration"] {
        background-image: none !important;
        background-color: transparent !important;
    }
    
    /* Make text inputs, buttons, and titles highly visible via high contrast colors */
    h1, h2, h3, span, p, label {
        font-family: 'Inter', -apple-system, sans-serif !important;
        color: #f1f5f9 !important; /* Premium off-white for crisp readability */
    }
    
    /* Force download button text to black for perfect visibility */
    div.stDownloadButton button p {
        color: #000000 !important;
    }
    
    /* Subtitles and micro-copy styling */
    .small-caption {
        color: #94a3b8 !important;
    }
    
    /* Sleek custom input card styling */
    div.stTextArea textarea {
        background-color: #144552 !important;
        color: #ffffff !important;
        border: 1px solid #065a60 !important;
        border-radius: 14px !important;
        font-size: 1.05rem !important;
    }
    
    /* Cyber Analyst Analysis Block Styling */
    div.stInfo {
        background-color: #212f45 !important;
        color: #f8fafc !important;
        border-left: 5px solid #006466 !important; /* Distinct rich teal indicator accent */
        border-radius: 12px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3) !important;
        padding: 24px !important;
    }
    
    /* Sidebar matching deep space gradient */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #144552 0%, #1b3a4b 100%) !important;
        border-right: 1px solid #0b525b !important;
    }
    
    /* History log container card styles in sidebar */
    .log-card {
        background-color: #1b3a4b;
        border: 1px solid #0b525b;
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    </style>
""", unsafe_allow_html=True)


# ---------------- UTILITY FUNCTIONS ----------------
def get_risk_color(score):
    if score <= 30:
        return "🟢 LOW"
    elif score <= 70:
        return "🟡 MEDIUM"
    else:
        return "🔴 HIGH"


# ---------------- SIDEBAR: DASHBOARD & ATTACK HISTORY ----------------
st.sidebar.markdown('<h1 style="font-size: 1.8rem; margin-bottom:0;">🛡️ CyberSentinel</h1>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="small-caption">Real-time Enterprise Prompt Firewall</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")

# Read logs
logs_data = []
if os.path.exists("analyzer/logs.json"):
    try:
        with open("analyzer/logs.json", "r") as f:
            logs_data = json.load(f)
    except Exception:
        pass

st.sidebar.metric("Total Prompt Scans", len(logs_data))
st.sidebar.markdown("---")

st.sidebar.markdown('<h3 style="font-size: 1.2rem;">📜 Recent Attack History</h3>', unsafe_allow_html=True)

if not logs_data:
    st.sidebar.info("No logs captured yet.")
else:
    for log in reversed(logs_data[-8:]):
        with st.sidebar.container():
            st.markdown(f"""
            <div class="log-card">
                <small style="color: #38bdf8;">🕒 {log.get('timestamp', 'N/A')}</small><br>
                <strong style="color: #f1f5f9;">Prompt:</strong> <span style="font-size: 0.9em; color: #cbd5e1;">{log.get('prompt', '')[:40]}...</span><br>
                <span style="font-size: 0.85em; color: #e2e8f0;">Score: <b style="color: #4ade80;">{log.get('score', 0)}/100</b></span>
            </div>
            """, unsafe_allow_html=True)


# ---------------- MAIN CONTENT INTERFACE ----------------
st.markdown('<h1 style="font-size: 2.5rem; letter-spacing: -0.5px;">🚀 Smart Prompt Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="small-caption" style="font-size: 1.1rem;">Inspect inputs dynamically for jailbreaks, parameter injections, and underlying threat payloads.</p>', unsafe_allow_html=True)

with st.container():
    prompt = st.text_area("Drop your model prompt here:", height=150, placeholder="Type or paste something suspicious...")

# ---------------- APPLICATION PIPELINE ----------------
if st.button("Run Threat Analysis", type="primary"):
    if not prompt:
        st.warning("Please enter a prompt structure to proceed.")
    else:
        col1, col2 = st.columns([3, 2], gap="large")
        
        # Pipeline calculations
        threats = detect_rules(prompt)
        score, severity = calculate_risk(threats)
        details = get_explanations(threats)

        if score > 0:
            ai_analysis = analyze_prompt(prompt, threats, score, severity)
        else:
            ai_analysis = "No vulnerabilities detected. This input aligns completely with safe structural operation models."

        save_log(prompt, threats, score, severity)

        # ---- LEFT PANEL: Threat Context & AI Engine ----
        with col1:
            st.markdown('<h2 style="font-size: 1.6rem; margin-top: 15px;">🤖 AI Security Analyst Report</h2>', unsafe_allow_html=True)
            st.info(ai_analysis)
            
            st.markdown('<h2 style="font-size: 1.6rem; margin-top: 25px;">🔍 Local Rule Engine Breakdowns</h2>', unsafe_allow_html=True)
            if not details:
                st.success("Clean prompt baseline! Zero signature matches detected.")
            else:
                for item in details:
                    st.markdown(f"""
                    <h3 style="color: #f43f5e; font-size: 1.2rem;">⚠️ {item['threat']}</h3>
                    <p style="color: #e2e8f0; margin-left: 10px;">💡 {item['explanation']}</p>
                    <hr style="border-color: #0b525b;">
                    """, unsafe_allow_html=True)

        # ---- RIGHT PANEL: Score Metric Vectors & Exports ----
        with col2:
            st.markdown('<h2 style="font-size: 1.6rem; margin-top: 15px;">📊 Risk Analysis</h2>', unsafe_allow_html=True)
            st.progress(score)
            
            m_col1, m_col2 = st.columns(2)
            m_col1.metric("Risk Score", f"{score}/100")
            m_col2.metric("Severity Level", get_risk_color(score))
            
            st.markdown("<hr style='border-color: #0b525b;'>", unsafe_allow_html=True)
            st.markdown('<h2 style="font-size: 1.6rem;">📋 Document Exports</h2>', unsafe_allow_html=True)
            
            try:
                pdf_file = generate_report(prompt, threats, score, severity, ai_analysis)
                st.success("Security Report PDF compiled.")
                
                with open(pdf_file, "rb") as file:
                    st.download_button(
                        label="📄 Download Security Report",
                        data=file,
                        file_name=os.path.basename(pdf_file),
                        mime="application/pdf",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Failed to generate enterprise PDF module: {e}")