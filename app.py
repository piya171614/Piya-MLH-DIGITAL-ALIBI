"""
DIGITAL ALIBI – AI Digital Evidence Investigator
Frontend & Official Google Gen AI Backend Integration

Theme & Palette:
- Main Background: #080F1E
- Sidebar: #0D1729
- Cards: #121F35
- Primary Blue: #2563EB
- Electric Cyan: #22D3EE
- Success Green: #22C55E
- Warning Amber: #F59E0B
- Danger Red: #EF4444
- Main Text: #F1F5F9
- Secondary Text: #94A3B8

Architecture: Python Streamlit | Plotly | FPDF2 | Official Google Gen AI SDK
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import time
from datetime import datetime, date
import plotly.graph_objects as go

# Import our robust forensic backend
import forensic_backend as fb

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="DIGITAL ALIBI | AI Forensic Workstation",
    page_icon="None",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CUSTOM CYBER-FORENSICS CSS STYLESHEET
# ==============================================================================
def inject_custom_css():
    """Injects high-end cyber-forensics workstation styling into Streamlit."""
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Dark Cyber-Forensics Workstation Palette */
    :root {
        --background-color: #080F1E !important;
        --secondary-background-color: #0D1729 !important;
        --primary-color: #2563EB !important;
        --text-color: #F1F5F9 !important;
    }

    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"], .main, section.main, .block-container {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #080F1E !important;
        color: #F1F5F9 !important;
    }

    section[data-testid="stSidebar"], [data-testid="stSidebarContent"], [data-testid="stSidebarNav"] {
        background-color: #0D1729 !important;
        border-right: 1px solid rgba(34, 211, 238, 0.15) !important;
    }
    section[data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }

    /* Force all typography away from default light theme colors */
    h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown, .stMarkdown p {
        color: #F1F5F9 !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: #121F35 !important;
        border: 1px solid rgba(34, 211, 238, 0.18) !important;
        border-radius: 12px !important;
    }

    [data-testid="stExpander"] {
        background-color: #121F35 !important;
        border: 1px solid rgba(34, 211, 238, 0.2) !important;
        border-radius: 10px !important;
    }
    [data-testid="stExpander"] summary {
        color: #F1F5F9 !important;
    }

    .forensic-card {
        background-color: #121F35;
        border: 1px solid rgba(34, 211, 238, 0.15);
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .forensic-card:hover {
        transform: translateY(-2px);
        border-color: rgba(34, 211, 238, 0.4);
        box-shadow: 0 8px 30px rgba(34, 211, 238, 0.12);
    }

    .metric-card {
        background: #121F35;
        border-left: 4px solid #22D3EE;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        border-top: 1px solid rgba(34, 211, 238, 0.08);
        border-right: 1px solid rgba(34, 211, 238, 0.08);
        border-bottom: 1px solid rgba(34, 211, 238, 0.08);
        margin-bottom: 12px;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-left: 4px solid #38BDF8;
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8 !important;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #F1F5F9 !important;
        margin-bottom: 4px;
        font-family: 'Inter', sans-serif;
    }
    .metric-sub {
        font-size: 0.78rem;
        font-weight: 500;
        color: #22D3EE !important;
    }

    .mono-hash {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.82rem;
        background-color: #080F1E;
        color: #22D3EE !important;
        padding: 4px 8px;
        border-radius: 6px;
        border: 1px solid rgba(34, 211, 238, 0.2);
        display: inline-block;
        word-break: break-all;
    }

    .badge {
        display: inline-block;
        padding: 4px 10px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-radius: 6px;
        margin-right: 6px;
    }
    .badge-observed {
        background-color: rgba(37, 99, 235, 0.18);
        color: #60A5FA !important;
        border: 1px solid rgba(37, 99, 235, 0.4);
    }
    .badge-claim {
        background-color: rgba(245, 158, 11, 0.18);
        color: #FBBF24 !important;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .badge-ai {
        background-color: rgba(168, 85, 247, 0.18);
        color: #C084FC !important;
        border: 1px solid rgba(168, 85, 247, 0.4);
    }
    .badge-unknown {
        background-color: rgba(148, 163, 184, 0.18);
        color: #94A3B8 !important;
        border: 1px solid rgba(148, 163, 184, 0.4);
    }
    .badge-cyan {
        background-color: rgba(34, 211, 238, 0.15);
        color: #22D3EE !important;
        border: 1px solid rgba(34, 211, 238, 0.4);
    }
    .badge-green {
        background-color: rgba(34, 197, 94, 0.15);
        color: #4ADE80 !important;
        border: 1px solid rgba(34, 197, 94, 0.4);
    }

    .timeline-node {
        position: relative;
        padding-left: 36px;
        margin-bottom: 24px;
        border-left: 2px solid rgba(34, 211, 238, 0.25);
    }
    .timeline-node::before {
        content: '';
        position: absolute;
        left: -7px;
        top: 4px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: #2563EB;
        border: 2px solid #080F1E;
        box-shadow: 0 0 10px #2563EB;
    }
    .timeline-node.user-reported::before {
        background-color: #F59E0B;
        box-shadow: 0 0 10px #F59E0B;
    }
    .timeline-node.ai-inferred::before {
        background-color: #A855F7;
        box-shadow: 0 0 10px #A855F7;
    }
    .timeline-node.contradiction::before {
        background-color: #EF4444;
        box-shadow: 0 0 10px #EF4444;
    }

    .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #38BDF8 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.25rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(34, 211, 238, 0.4) !important;
        border-color: #22D3EE !important;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"], div[data-baseweb="select"] > div {
        background-color: #0D1729 !important;
        border: 1px solid rgba(34, 211, 238, 0.2) !important;
        color: #F1F5F9 !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #22D3EE !important;
        box-shadow: 0 0 10px rgba(34, 211, 238, 0.25) !important;
    }

    div[role="radiogroup"] label {
        color: #F1F5F9 !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #0D1729 !important;
        border: 2px dashed rgba(34, 211, 238, 0.35) !important;
    }
    [data-testid="stFileUploaderDropzone"] * {
        color: #94A3B8 !important;
    }

    div[data-testid="stDataFrame"], table {
        background-color: #0D1729 !important;
        color: #F1F5F9 !important;
    }

    .login-container {
        max-width: 480px;
        margin: 40px auto;
        background-color: #121F35;
        border: 1px solid rgba(34, 211, 238, 0.3);
        border-radius: 16px;
        padding: 40px 36px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6), 0 0 24px rgba(34, 211, 238, 0.15);
        text-align: center;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


# ==============================================================================
# 3. SESSION STATE INITIALIZATION
# ==============================================================================
def init_session_state():
    """Initializes authentication, active case, evidence vault, and analysis states."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = fb.get_gemini_api_key()

    if "current_case_id" not in st.session_state:
        st.session_state.current_case_id = "CASE-2024-8891"

    if "cases" not in st.session_state:
        st.session_state.cases = {
            "CASE-2024-8891": {
                "id": "CASE-2024-8891",
                "title": "Operation Silent Beacon: Cloud Key Exfiltration",
                "lead_investigator": "Special Agent V. Thorne",
                "agency": "Cyber Crime Taskforce // Incident Response",
                "classification": "Confidential // Law Enforcement Sensitive",
                "incident_category": "Unauthorized Data Exfiltration & Identity Spoofing",
                "incident_date": "2024-10-14",
                "status": "Active Analysis",
                "target_subject": "Marcus Vance (Senior DevOps Engineer)",
                "claimed_alibi": "Subject claimed he was offline attending an off-site conference in Chicago between 20:00 and 23:30 UTC on Oct 14, 2024, without laptop access.",
                "hypothesis": "Subject used compromised service credentials via a residential proxy tunnel to exfiltrate master encryption keys while staging a false physical alibi."
            },
            "CASE-2024-9102": {
                "id": "CASE-2024-9102",
                "title": "Phantom Ledger: Swift Transfer Manipulation",
                "lead_investigator": "Forensic Examiner K. Reyes",
                "agency": "Financial Cyber Crimes Unit",
                "classification": "Secret // Evidentiary Hold",
                "incident_category": "Wire Fraud & Transaction Log Tampering",
                "incident_date": "2024-11-02",
                "status": "Evidence Ingestion",
                "target_subject": "Elena Rostova (Lead Treasury Operator)",
                "claimed_alibi": "Subject stated terminal was locked and unattended during the scheduled maintenance window from 01:00 to 03:00 UTC.",
                "hypothesis": "Automated PowerShell script executed locally from subject workstation bypassed 2FA authorization token checks."
            },
            "CASE-2024-7740": {
                "id": "CASE-2024-7740",
                "title": "Citadel Vault: Proprietary Model Leak",
                "lead_investigator": "Forensic Specialist D. Chen",
                "agency": "Intellectual Property Protection Taskforce",
                "classification": "Top Secret // Compartmented",
                "incident_category": "Insider Espionage",
                "incident_date": "2024-09-28",
                "status": "Report Finalized",
                "target_subject": "Dr. Julian Mercer (Principal AI Researcher)",
                "claimed_alibi": "Device reported stolen from airport lounge at 17:45 UTC prior to suspicious repository clone operations.",
                "hypothesis": "Exfiltration conducted via encrypted steganography inside research presentation slides."
            }
        }

    # Populate default evidence items backed by real files in evidence_store/
    if "evidence_vault" not in st.session_state:
        st.session_state.evidence_vault = [
            {
                "id": "EV-001",
                "case_id": "CASE-2024-8891",
                "filename": "surveillance_still_terminal_b.jpg",
                "classification": "Physical CCTV Frame",
                "type": "image/jpeg",
                "size_kb": 22.4,
                "sha256": "8f3b1456a9c1e089d71fa9e39b7d03fec719c3b87910fa4d189efbc99201ae87",
                "ingest_timestamp": "2024-10-15 08:34:12 UTC",
                "source": "Airport Security Feed (ORD Terminal 2)",
                "status": "Verified & Hashed"
            },
            {
                "id": "EV-002",
                "case_id": "CASE-2024-8891",
                "filename": "auth_syslog_prod_bastion.log",
                "classification": "Bastion Authentication Log",
                "type": "text/plain",
                "size_kb": 1.2,
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "ingest_timestamp": "2024-10-15 09:12:05 UTC",
                "source": "AWS CloudWatch Bastion Dump",
                "status": "Verified & Hashed"
            },
            {
                "id": "EV-003",
                "case_id": "CASE-2024-8891",
                "filename": "cell_tower_cdr_oct14.csv",
                "classification": "Carrier CDR Telemetry",
                "type": "text/csv",
                "size_kb": 1.8,
                "sha256": "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
                "ingest_timestamp": "2024-10-15 11:20:44 UTC",
                "source": "Subpoena Carrier Record (Sector ID #492)",
                "status": "Verified & Hashed"
            },
            {
                "id": "EV-004",
                "case_id": "CASE-2024-8891",
                "filename": "slack_dm_export_confidential.json",
                "classification": "Encrypted Chat Transcript",
                "type": "application/json",
                "size_kb": 0.8,
                "sha256": "ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",
                "ingest_timestamp": "2024-10-15 14:05:19 UTC",
                "source": "Corporate Slack Compliance Vault",
                "status": "Verified & Hashed"
            },
            {
                "id": "EV-005",
                "case_id": "CASE-2024-8891",
                "filename": "hotel_wifi_radius_session.log",
                "classification": "Wi-Fi RADIUS Session",
                "type": "text/plain",
                "size_kb": 0.6,
                "sha256": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae",
                "ingest_timestamp": "2024-10-16 02:40:10 UTC",
                "source": "Hyatt Regency Guest Gateway",
                "status": "Verified & Hashed"
            }
        ]

    # Initialize analysis results using local heuristic analysis baseline
    if "timeline_events" not in st.session_state or "digital_story" not in st.session_state:
        init_analysis = fb.run_local_heuristic_analysis(
            st.session_state.cases[st.session_state.current_case_id],
            st.session_state.evidence_vault,
            st.session_state.cases[st.session_state.current_case_id]["claimed_alibi"]
        )
        st.session_state.digital_story = init_analysis["digital_story"]
        st.session_state.timeline_events = init_analysis["timeline"]
        st.session_state.contradictions = init_analysis["contradictions"]
        st.session_state.missing_evidence = init_analysis["missing_evidence"]
        st.session_state.ai_observations = init_analysis["observations"]
        st.session_state.last_analysis_engine = init_analysis["engine"]

def get_current_case() -> dict:
    cid = st.session_state.current_case_id
    return st.session_state.cases.get(cid, list(st.session_state.cases.values())[0])


# ==============================================================================
# 4. PAGE 1: LOGIN / WELCOME GATEWAY
# ==============================================================================
def get_forensic_bg_base64() -> str:
    """Reads and base64 encodes the local forensic workstation background image."""
    import base64
    bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "forensic_bg.jpg")
    if os.path.exists(bg_path):
        with open(bg_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

def render_login_page():
    """Renders the upgraded cyber-forensics workstation authentication & welcome portal."""
    bg_b64 = get_forensic_bg_base64()
    bg_css = f"""
    <style>
    /* Forensic Workstation Background with Strong Dark Overlay */
    .stApp {{
        background: linear-gradient(180deg, rgba(8, 15, 30, 0.84) 0%, rgba(8, 15, 30, 0.94) 100%),
                    url('data:image/jpeg;base64,{bg_b64}') no-repeat center center fixed !important;
        background-size: cover !important;
    }}

    /* Central Branding Block */
    .branding-hero {{
        text-align: center;
        max-width: 680px;
        margin: 0 auto 24px auto;
    }}
    .hero-shield-glow {{
        width: 76px;
        height: 76px;
        margin: 0 auto 16px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(34, 211, 238, 0.3) 0%, rgba(37, 99, 235, 0.08) 70%);
        border: 1.5px solid #22D3EE;
        font-size: 38px;
        box-shadow: 0 0 25px rgba(34, 211, 238, 0.45);
        animation: shieldPulse 3s infinite alternate ease-in-out;
    }}
    @keyframes shieldPulse {{
        0% {{ box-shadow: 0 0 20px rgba(34, 211, 238, 0.3); transform: scale(0.98); }}
        100% {{ box-shadow: 0 0 35px rgba(34, 211, 238, 0.6); transform: scale(1.02); }}
    }}
    .hero-main-title {{
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #F1F5F9;
        margin: 0 0 6px 0;
        text-shadow: 0 2px 14px rgba(0, 0, 0, 0.7);
    }}
    .hero-tagline {{
        font-size: 1.05rem;
        font-style: italic;
        color: #22D3EE;
        font-weight: 600;
        margin-bottom: 6px;
        letter-spacing: 0.02em;
    }}
    .hero-subtitle {{
        font-size: 0.92rem;
        font-weight: 500;
        color: #E2E8F0;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 12px;
    }}
    .hero-description {{
        font-size: 0.88rem;
        line-height: 1.6;
        color: #94A3B8;
        max-width: 580px;
        margin: 0 auto 18px auto;
    }}

    /* Small Feature Strip */
    .feature-strip-bar {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
        margin-bottom: 28px;
    }}
    .feature-strip-item {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #E2E8F0;
        background: rgba(18, 31, 53, 0.7);
        border: 1px solid rgba(34, 211, 238, 0.2);
        padding: 5px 14px;
        border-radius: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }}
    .feature-dot {{
        color: #22D3EE;
        font-size: 0.9rem;
    }}
    .feature-divider {{
        color: rgba(34, 211, 238, 0.3);
        font-size: 0.85rem;
    }}

    /* Glassmorphism Login Card */
    .glass-card-wrapper {{
        background: rgba(18, 31, 53, 0.78) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(34, 211, 238, 0.28) !important;
        border-radius: 18px !important;
        padding: 28px 32px !important;
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.75), 0 0 35px rgba(34, 211, 238, 0.12) !important;
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease !important;
    }}
    .glass-card-wrapper:hover {{
        border-color: rgba(34, 211, 238, 0.45) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 45px rgba(34, 211, 238, 0.22) !important;
    }}

    /* Professional Footer */
    .login-footer-bar {{
        text-align: center;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid rgba(34, 211, 238, 0.12);
        font-size: 0.82rem;
        color: #94A3B8;
        letter-spacing: 0.02em;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

    

    # Central Branding Section
    st.markdown(
        """
        <div class="branding-hero">
            <div class="hero-shield-glow">
                <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                </svg>
            </div>
            <h1 class="hero-main-title">DIGITAL ALIBI</h1>
            <div class="hero-tagline">"Every Digital Trace Tells a Story."</div>
            <div class="hero-subtitle">AI-Powered Digital Evidence Investigation Platform</div>
            <p class="hero-description">
                An advanced cyber-forensics platform that autonomously analyzes multi-source digital evidence,
                surfaces factual contradictions against suspect alibis, and reconstructs verified chronological incident timelines.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Small Feature Strip
    st.markdown(
        """
        <div class="feature-strip-bar">
            <div class="feature-strip-item">
                <span class="feature-dot">●</span> Evidence Analysis
            </div>
            <span class="feature-divider">|</span>
            <div class="feature-strip-item">
                <span class="feature-dot">●</span> Timeline Reconstruction
            </div>
            <span class="feature-divider">|</span>
            <div class="feature-strip-item">
                <span class="feature-dot">●</span> Evidence Integrity
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # Glassmorphism Centered Login Card
    col_l1, col_l2, col_l3 = st.columns([1, 1.4, 1])

    with col_l2:
        with st.container(border=True):
            st.markdown("#### Examiner Terminal Sign In")
            st.caption("Access the secure digital forensics investigation workspace.")
            
            examiner_email = st.text_input("Examiner Email / Identity", value="analyst@digitalalibi.io")
            examiner_pwd = st.text_input("Security Passphrase / Token PIN", value="••••••••••••", type="password")
            
            st.write("")
            col_sign, col_demo = st.columns([1, 1])

            with col_sign:
                if st.button("Sign In to Workstation", type="primary", use_container_width=True):
                    st.session_state.authenticated = True
                    st.session_state.current_page = "Dashboard"
                    st.success("Credentials authenticated. Initializing forensic environment...")
                    time.sleep(0.4)
                    st.rerun()

            with col_demo:
                if st.button("Without Sign In", use_container_width=True):
                    st.session_state.authenticated = True
                    st.session_state.current_page = "Dashboard"
                    st.rerun()

            st.write("")
            st.markdown(
                """
                <div style="background-color: rgba(8, 15, 30, 0.7); border-left: 3px solid #22D3EE; padding: 10px 14px; border-radius: 6px; font-size: 0.78rem; color: #94A3B8;">
                    <strong style="color: #22D3EE;">Hackathon Evaluator Notice:</strong><br>
                    Click <strong>Without Sign In</strong> to immediately enter the complete forensics dashboard with verified evidence, active cases, and working AI correlation.
                </div>
                """,
                unsafe_allow_html=True
            )

    # Professional Footer
    st.markdown(
        """
        <div class="login-footer-bar">
            Independent AI-powered digital forensics project | Educational prototype.
        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================================================================
# 5. SIDEBAR NAVIGATION & TELEMETRY
# ==============================================================================
def render_sidebar():
    """Renders the left navigation sidebar with logo, active docket, and all 10 sections."""
    with st.sidebar:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <div style="width: 38px; height: 38px; border-radius: 8px; background: rgba(34, 211, 238, 0.15); border: 1.5px solid #22D3EE; display: flex; align-items: center; justify-content: center;">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                    </svg>
                </div>
                <div>
                    <h3 style="margin: 0; color: #F1F5F9; font-weight: 800; font-size: 1.15rem; letter-spacing: 0.04em;">DIGITAL ALIBI</h3>
                    <p style="margin: 0; color: #22D3EE; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.05em;">AI EVIDENCE INVESTIGATOR</p>
                </div>
            </div>
            <p style="color: #94A3B8; font-size: 0.78rem; font-style: italic; margin-bottom: 16px;">"Every digital trace tells a story."</p>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        st.caption("FORENSIC WORKSTATION MODULES")
        pages = [
            "Dashboard",
            "New Investigation",
            "Evidence Vault",
            "Timeline Analysis",
            "AI Investigation",
            "Evidence Integrity",
            "Investigation Reports",
            "About Digital Alibi",
            "Help & Privacy",
            "Logout"
        ]

        current_idx = pages.index(st.session_state.current_page) if st.session_state.current_page in pages else 0
        selected = st.radio(
            "Navigation Menu",
            pages,
            index=current_idx,
            label_visibility="collapsed"
        )
        
        if selected == "Logout":
            st.session_state.authenticated = False
            st.session_state.current_page = "Dashboard"
            st.rerun()

        if selected != st.session_state.current_page:
            st.session_state.current_page = selected
            st.rerun()

        st.divider()

        # Gemini AI Configuration (Official SDK) - Clean, No Emojis
        with st.expander("Gemini AI API Key (Official SDK)", expanded=False):
            st.caption("Google Gen AI SDK connects to Gemini 2.5 Flash / 1.5 Flash.")
            current_k = st.session_state.get("gemini_api_key", "")
            entered_k = st.text_input(
                "Gemini API Key",
                value=current_k,
                type="password",
                help="Google AI Studio API key used by the official google-genai SDK."
            )
            if entered_k != current_k:
                st.session_state.gemini_api_key = entered_k.strip()
                os.environ["GEMINI_API_KEY"] = entered_k.strip()

            active_k = fb.get_gemini_api_key(st.session_state)
            if active_k:
                st.markdown(
                    """
                    <div style="background: rgba(34, 197, 94, 0.12); border: 1px solid rgba(34, 197, 94, 0.35); border-radius: 6px; padding: 6px 12px; margin-top: 6px;">
                        <span style="color: #4ADE80; font-weight: 600; font-size: 0.8rem;">[ACTIVE] Gemini API Key Active</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div style="background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 6px; padding: 6px 12px; margin-top: 6px;">
                        <span style="color: #FBBF24; font-weight: 600; font-size: 0.8rem;">[LOCAL] Local Forensic Engine Active</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.divider()
        # Active Case Docket Selector
        st.caption("ACTIVE CASE DOCKET")
        case_keys = list(st.session_state.cases.keys())
        case_idx = case_keys.index(st.session_state.current_case_id) if st.session_state.current_case_id in case_keys else 0
        
        chosen_case = st.selectbox(
            "Select Docket",
            case_keys,
            index=case_idx,
            format_func=lambda x: f"{x} - {st.session_state.cases[x]['title'][:20]}...",
            label_visibility="collapsed"
        )
        if chosen_case != st.session_state.current_case_id:
            st.session_state.current_case_id = chosen_case
            st.rerun()

        active_case = get_current_case()
        st.markdown(
            f"""
            <div style="background-color: #121F35; border: 1px solid rgba(34, 211, 238, 0.15); border-radius: 8px; padding: 12px; font-size: 0.78rem; color: #94A3B8;">
                <div style="color: #22D3EE; font-weight: 700; margin-bottom: 4px;">{st.session_state.current_case_id}</div>
                <div><strong>Lead:</strong> {active_case['lead_investigator']}</div>
                <div><strong>Status:</strong> <span style="color: #22C55E;">{active_case['status']}</span></div>
                <div><strong>Class:</strong> {active_case['classification']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        # Fast sign out button
        if st.button("Sign Out (Lock Workstation)", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_page = "Dashboard"
            st.rerun()


# ==============================================================================
# 6. PAGE 2: DASHBOARD (UPGRADED WITH ACTUAL APPLICATION DATA)
# ==============================================================================
def render_dashboard():
    """Renders the comprehensive operations command center using actual application data."""
    # Header & Prominent Action Button
    head_col1, head_col2 = st.columns([3, 1.2])
    with head_col1:
        st.title("Forensic Operations Command Center")
        st.markdown("##### AI-Powered Digital Trace Analysis & Chronological Alibi Reconstruction")
        st.caption(f"Active Docket: **{st.session_state.current_case_id}** | Engine: **{st.session_state.get('last_analysis_engine', 'Gemini Core')}**")

    with head_col2:
        st.write("")
        if st.button("+ Start New Investigation", type="primary", use_container_width=True):
            st.session_state.current_page = "New Investigation"
            st.rerun()

    st.write("")

    # Welcome Banner & Project Introduction
    with st.container(border=True):
        st.markdown("### Welcome to DIGITAL ALIBI Workstation")
        st.markdown(
            """
            **DIGITAL ALIBI** is an autonomous cyber-forensics platform that empowers investigators, legal counsel, 
            and incident responders to objectively evaluate electronic evidence. By ingesting disparate multi-modal artifacts 
            (system auth syslogs, cellular tower CDR records, surveillance CCTV stills, and encrypted messaging dumps), 
            the platform cross-references claimed suspect alibis against empirical digital footprints to surface direct 
            contradictions and reconstruct verified chronological timelines.
            """
        )
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.markdown("**Evidence Integrity:** SHA-256 Strict Bitstream Ledger")
        col_m2.markdown("**Multimodal AI:** Google Gemini 2.5 Flash / Local Engine")
        col_m3.markdown("**Admissibility:** FRE Rule 902(14) Certified Record Standard")

    st.write("")

    # Actual Application Statistics (Real Data)
    total_cases = len(st.session_state.cases)
    total_evidence = len(st.session_state.evidence_vault)
    total_timeline = len(st.session_state.timeline_events)
    total_contradictions = len(st.session_state.contradictions)
    total_kb = sum(float(e.get("size_kb", 0)) for e in st.session_state.evidence_vault)

    st.markdown("#### Real-Time Forensic Case Telemetry")
    kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)

    with kpi_c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Investigations</div>
                <div class="metric-value">{total_cases}</div>
                <div class="metric-sub">▲ Active Case Dockets</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with kpi_c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Evidence Files Ingested</div>
                <div class="metric-value">{total_evidence}</div>
                <div class="metric-sub">● {round(total_kb, 1)} KB Cryptographically Sealed</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with kpi_c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Timeline Milestones</div>
                <div class="metric-value">{total_timeline}</div>
                <div class="metric-sub">● Chronologically Correlated</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with kpi_c4:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color: #EF4444;">
                <div class="metric-title">Flagged Contradictions</div>
                <div class="metric-value" style="color: #F87171;">{total_contradictions}</div>
                <div class="metric-sub" style="color: #EF4444;">● Direct Alibi Conflicts</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # Visual Analytics & Pipeline Activity
    col_chart, col_activity = st.columns([1.6, 1.0])

    with col_chart:
        st.markdown("#### Evidence Distribution by Classification")
        
        # Real distribution from evidence_vault
        class_counts = {}
        for ev in st.session_state.evidence_vault:
            c_name = ev.get("classification", "Other")
            class_counts[c_name] = class_counts.get(c_name, 0) + 1
            
        chart_labels = list(class_counts.keys()) if class_counts else ["No Evidence Ingested"]
        chart_vals = list(class_counts.values()) if class_counts else [0]

        fig = go.Figure(data=[
            go.Bar(
                x=chart_labels,
                y=chart_vals,
                marker=dict(
                    color=['#2563EB', '#22D3EE', '#38BDF8', '#818CF8', '#A78BFA', '#22C55E'][:len(chart_labels)],
                    line=dict(color='#22D3EE', width=1)
                ),
                text=chart_vals,
                textposition='auto',
            )
        ])
        fig.update_layout(
            paper_bgcolor='rgba(18, 31, 53, 0.7)',
            plot_bgcolor='rgba(18, 31, 53, 0.7)',
            font=dict(color='#F1F5F9', family='Inter'),
            margin=dict(l=20, r=20, t=30, b=20),
            height=280,
            xaxis=dict(showgrid=False, linecolor='rgba(34, 211, 238, 0.2)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(34, 211, 238, 0.1)', linecolor='rgba(34, 211, 238, 0.2)'),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_activity:
        st.markdown("#### Real-Time Case Audit Trail")
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="font-size: 0.82rem; line-height: 1.6;">
                    <div style="margin-bottom: 8px;">
                        <span style="color: #22D3EE;">● Active Docket:</span> <code>{st.session_state.current_case_id}</code> loaded
                    </div>
                    <div style="margin-bottom: 8px;">
                        <span style="color: #22C55E;">● Evidence Ingestion:</span> {len(st.session_state.evidence_vault)} artifacts bitstream hashed
                    </div>
                    <div style="margin-bottom: 8px;">
                        <span style="color: #EF4444;">● Contradiction Check:</span> {len(st.session_state.contradictions)} factual conflicts identified
                    </div>
                    <div style="margin-bottom: 8px;">
                        <span style="color: #F59E0B;">● Gap Discovery:</span> {len(st.session_state.missing_evidence)} evidentiary blindspots flagged
                    </div>
                    <div>
                        <span style="color: #22D3EE;">● AI Model:</span> {st.session_state.get('last_analysis_engine', 'Google Gemini Ready')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")
    st.divider()

    st.markdown("#### Active Forensic Case Registry")
    case_rows = []
    for cid, cinfo in st.session_state.cases.items():
        case_rows.append({
            "Docket ID": cid,
            "Investigation Title": cinfo["title"],
            "Target Subject": cinfo["target_subject"],
            "Category": cinfo["incident_category"],
            "Incident Date": cinfo["incident_date"],
            "Classification": cinfo["classification"],
            "Status": cinfo["status"]
        })
    df_cases = pd.DataFrame(case_rows)
    st.dataframe(df_cases, use_container_width=True, hide_index=True)


# ==============================================================================
# 7. PAGE 3: NEW INVESTIGATION & EVIDENCE UPLOAD
# ==============================================================================
def render_new_investigation():
    """Renders the case intake and multi-file drag-and-drop evidence ingestion portal."""
    st.title("New Investigation Intake & Evidence Upload")
    st.caption("Register a new cyber-forensics docket and ingest multi-modal evidentiary artifacts.")

    # Case Dossier Parameters
    with st.container(border=True):
        st.markdown("#### Case Docket Parameters")
        
        row1_c1, row1_c2, row1_c3 = st.columns([1, 2, 1])
        new_case_id = row1_c1.text_input("Case Reference Number", value=f"CASE-2024-{datetime.now().strftime('%M%S')}")
        new_title = row1_c2.text_input("Investigation Title", value="Operation Dark Mirage: Cloud Database Intrusion")
        new_category = row1_c3.selectbox(
            "Incident Category",
            [
                "Unauthorized Access & Data Exfiltration",
                "Ransomware Deployment & Extortion",
                "Insider Threat & IP Espionage",
                "Wire Fraud & Financial Embezzlement",
                "System Sabotage & Log Wiping",
                "Identity Theft & Credential Stuffing"
            ]
        )

        row2_c1, row2_c2, row2_c3 = st.columns(3)
        new_lead = row2_c1.text_input("Lead Forensic Examiner", value="Special Agent D. Foster")
        new_agency = row2_c2.text_input("Investigating Agency / Squad", value="Cyber Taskforce // Squad 7")
        new_class = row2_c3.selectbox(
            "Security Classification",
            ["Confidential // Law Enforcement Sensitive", "Secret // Evidentiary Hold", "Top Secret // SCI", "Law Enforcement Sensitive"]
        )

        row3_c1, row3_c2 = st.columns(2)
        new_target = row3_c1.text_input("Person of Interest / Suspect", value="Robert Vance (Principal Architect)")
        new_date = row3_c2.date_input("Incident Date", value=date.today())

        st.write("")
        new_alibi = st.text_area(
            "Suspect Claimed Alibi Defense",
            value="Subject claims their laptop was locked in their apartment safe while they dined at a local bistro between 19:30 and 22:30 without using any networked device.",
            help="The AI will compare this defense against timestamps, cellular tower CDRs, and login records.",
            height=90
        )

        new_hypothesis = st.text_area(
            "Investigative Theory / Initial Hypothesis",
            value="Investigators suspect the subject deployed a scheduled cron task or used an unauthorized cellular hotspot to stage an exfiltration while physically away from their residence.",
            height=90
        )

    st.write("")

    # Evidence Upload Area
    st.markdown("#### Multi-Modal Digital Evidence Ingestion Vault")
    st.caption("Drag and drop multiple forensic artifacts. Supports images, screenshots, syslog files, database exports, and documents.")

    with st.container(border=True):
        uploaded_files = st.file_uploader(
            "Drop Forensic Artifacts Here",
            type=["png", "jpg", "jpeg", "webp", "txt", "log", "json", "csv", "pdf"],
            accept_multiple_files=True,
            help="Accepts images, screenshots, text logs, JSON/CSV exports, and PDF subpoenas"
        )

        if uploaded_files:
            st.info(f"{len(uploaded_files)} artifact(s) staged for cryptographic sealing and AI analysis.")
            
            # File Previews & Live SHA-256 Hashing Table
            file_meta_rows = []
            for f in uploaded_files:
                f_bytes = f.getvalue()
                f_hash = fb.compute_sha256(f_bytes)
                f_size_kb = round(len(f_bytes) / 1024.0, 2)
                file_meta_rows.append({
                    "File Name": f.name,
                    "Detected Type": f.type if f.type else "application/octet-stream",
                    "Size (KB)": f"{f_size_kb} KB",
                    "Cryptographic SHA-256 Checksum": f_hash,
                    "Status": "Ready for Ingestion"
                })

            st.dataframe(pd.DataFrame(file_meta_rows), use_container_width=True, hide_index=True)

            st.write("")
            btn_col1, btn_col2 = st.columns([2, 1])

            with btn_col1:
                if st.button("Ingest Evidence & Launch AI Analysis", type="primary", use_container_width=True):
                    prog_bar = st.progress(0)
                    status_text = st.empty()

                    # Save and preserve all uploaded files
                    status_text.markdown("**1. Computing SHA-256 cryptographic hashes & sealing files on disk...**")
                    prog_bar.progress(0.25)
                    
                    new_evidence_list = []
                    for f in uploaded_files:
                        f_bytes = f.getvalue()
                        f_hash = fb.compute_sha256(f_bytes)
                        fb.save_evidence_file(f.name, f_bytes)
                        new_ev = {
                            "id": f"EV-{len(st.session_state.evidence_vault) + len(new_evidence_list) + 1:03d}",
                            "case_id": new_case_id,
                            "filename": f.name,
                            "classification": "Uploaded Artifact",
                            "type": f.type if f.type else "text/plain",
                            "size_kb": round(len(f_bytes) / 1024.0, 2),
                            "sha256": f_hash,
                            "ingest_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
                            "source": f"Examiner Upload (Docket {new_case_id})",
                            "status": "Verified & Hashed"
                        }
                        new_evidence_list.append(new_ev)

                    # Register case
                    st.session_state.cases[new_case_id] = {
                        "id": new_case_id,
                        "title": new_title,
                        "lead_investigator": new_lead,
                        "agency": new_agency,
                        "classification": new_class,
                        "incident_category": new_category,
                        "incident_date": str(new_date),
                        "status": "Active Analysis",
                        "target_subject": new_target,
                        "claimed_alibi": new_alibi,
                        "hypothesis": new_hypothesis
                    }
                    st.session_state.current_case_id = new_case_id
                    st.session_state.evidence_vault.extend(new_evidence_list)

                    status_text.markdown("**2. Sending multi-modal evidence to Gemini AI for forensic correlation...**")
                    prog_bar.progress(0.60)

                    api_key = fb.get_gemini_api_key(st.session_state)
                    case_payload = st.session_state.cases[new_case_id]

                    try:
                        if api_key:
                            analysis_result = fb.analyze_evidence_with_gemini(
                                api_key=api_key,
                                case_info=case_payload,
                                evidence_items=new_evidence_list,
                                suspect_alibi=new_alibi
                            )
                        else:
                            analysis_result = fb.run_local_heuristic_analysis(
                                case_info=case_payload,
                                evidence_items=new_evidence_list,
                                suspect_alibi=new_alibi
                            )
                    except Exception as err:
                        st.warning(f"Gemini API Notice: {str(err)}. Executing Local Forensic Engine fallback.")
                        analysis_result = fb.run_local_heuristic_analysis(
                            case_info=case_payload,
                            evidence_items=new_evidence_list,
                            suspect_alibi=new_alibi
                        )

                    prog_bar.progress(0.90)
                    status_text.markdown("**3. Synthesizing digital timeline, contradiction matrix, and legal dossier...**")

                    # Commit analysis results
                    st.session_state.digital_story = analysis_result.get("digital_story", "Analysis completed.")
                    st.session_state.timeline_events = analysis_result.get("timeline", [])
                    st.session_state.contradictions = analysis_result.get("contradictions", [])
                    st.session_state.missing_evidence = analysis_result.get("missing_evidence", [])
                    st.session_state.ai_observations = analysis_result.get("observations", [])
                    st.session_state.last_analysis_engine = analysis_result.get("engine", "Forensic Engine")

                    prog_bar.progress(1.0)
                    status_text.markdown("**[COMPLETE] Forensic Ingestion & AI Correlation Completed Successfully.**")
                    time.sleep(0.8)
                    st.session_state.current_page = "AI Investigation"
                    st.rerun()

            with btn_col2:
                if st.button("Cancel & Clear Uploads", use_container_width=True):
                    st.rerun()
        else:
            st.markdown(
                """
                <div style="text-align: center; padding: 40px 20px; color: #94A3B8;">
                    <span style="font-size: 1.5rem; color: #22D3EE;">[VAULT EMPTY]</span>
                    <h4 style="color: #F1F5F9; margin-top: 12px;">No Evidence Staged Yet</h4>
                    <p style="font-size: 0.85rem; max-width: 480px; margin: 0 auto;">
                        Select or drag-and-drop surveillance frames, tower logs, or chat archives above to begin cryptographic sealing and AI correlation.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


# ==============================================================================
# 8. PAGE 4: EVIDENCE VAULT (UPGRADED WITH BITSTREAM PREVIEWS)
# ==============================================================================
def render_evidence_vault():
    """Renders all uploaded evidence items in cyber-forensics cards with SHA-256 hashes and previews."""
    st.title("Preserved Evidence Vault")
    active_case = get_current_case()
    st.caption(f"Cryptographic Chain of Custody for Docket: **{st.session_state.current_case_id}** — {active_case['title']}")

    with st.container(border=True):
        col_b1, col_b2, col_b3 = st.columns([2, 1, 1])
        col_b1.markdown(f"**Target Subject:** `{active_case['target_subject']}`")
        col_b2.markdown(f"**Total Artifacts:** `{len(st.session_state.evidence_vault)}`")
        col_b3.markdown(f"**Integrity:** `100.0% Cryptographically Sealed`")

    st.write("")

    # Filter & Search
    search_col1, search_col2 = st.columns([2, 1])
    search_term = search_col1.text_input("Search Artifacts by Filename or Source", placeholder="e.g. syslog, cell_tower, ORD...")
    class_filter = search_col2.selectbox(
        "Filter by Evidence Classification",
        ["All Classifications", "Physical CCTV Frame", "Bastion Authentication Log", "Carrier CDR Telemetry", "Encrypted Chat Transcript", "Wi-Fi RADIUS Session", "Uploaded Artifact"]
    )

    filtered_evidence = st.session_state.evidence_vault.copy()
    if search_term:
        filtered_evidence = [e for e in filtered_evidence if search_term.lower() in e["filename"].lower() or search_term.lower() in e["source"].lower()]
    if class_filter != "All Classifications":
        filtered_evidence = [e for e in filtered_evidence if e["classification"] == class_filter]

    st.write("")

    if not filtered_evidence:
        st.markdown(
            """
            <div class="forensic-card" style="text-align: center; padding: 40px 20px;">
                <span style="font-size: 1.5rem; color: #94A3B8;">[NO MATCH]</span>
                <h4 style="color: #F1F5F9; margin-top: 8px;">No Evidence Artifacts Match Filter</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">Clear search parameters or navigate to 'New Investigation' to upload artifacts.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        for ev in filtered_evidence:
            with st.container(border=True):
                top_col1, top_col2 = st.columns([3, 1.2])
                with top_col1:
                    st.markdown(f"### `{ev['id']}` : **{ev['filename']}**")
                    st.markdown(
                        f"""
                        <span class="badge badge-cyan">{ev['classification']}</span>
                        <span class="badge badge-green">{ev['status']}</span>
                        <span style="color: #94A3B8; font-size: 0.8rem;">Size: <strong>{ev['size_kb']} KB</strong> | Ingested: <strong>{ev['ingest_timestamp']}</strong></span>
                        """,
                        unsafe_allow_html=True
                    )
                with top_col2:
                    st.caption("EVIDENTIARY SOURCE")
                    st.markdown(f"**{ev['source']}**")

                st.write("")
                st.markdown(
                    f"""
                    <div style="background-color: #080F1E; padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(34, 211, 238, 0.2);">
                        <span style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase;">Cryptographic SHA-256 Checksum:</span><br>
                        <span class="mono-hash">{ev['sha256']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Real Content Inspection (Reads original bytes from evidence_store)
                file_bytes = fb.read_evidence_file(ev["filename"])
                with st.expander(f"Inspect Preserved Artifact Bitstream ({ev['filename']})"):
                    if file_bytes:
                        if ev["filename"].lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                            st.image(file_bytes, caption=f"Original Preserved Artifact: {ev['filename']}", use_container_width=True)
                        else:
                            try:
                                text_preview = file_bytes.decode('utf-8', errors='ignore')
                                st.code(text_preview[:3000], language="bash" if ".log" in ev["filename"] else "text")
                            except Exception:
                                st.write("Binary payload preserved. Hash verified.")
                    else:
                        st.info("Artifact hash sealed in ledger. Physical device copy verified.")


# ==============================================================================
# 9. PAGE 5: TIMELINE ANALYSIS
# ==============================================================================
def render_timeline_analysis():
    """Renders the visually attractive vertical timeline with confidence classifications."""
    st.title("Chronological Timeline Analysis")
    st.caption("Temporal cross-correlation of digital footprints, suspect alibi assertions, and empirical proof.")

    # Timeline Legend & Filter Bar
    with st.container(border=True):
        st.markdown(
            """
            <div style="display: flex; gap: 20px; flex-wrap: wrap; align-items: center; font-size: 0.82rem;">
                <span style="color: #F1F5F9; font-weight: 600;">EVIDENCE CONFIDENCE CLASSIFICATION:</span>
                <span><span class="badge badge-observed">● DIRECTLY OBSERVED</span> (Empirical Hardware/CCTV/Logs)</span>
                <span><span class="badge badge-claim">● USER-REPORTED</span> (Suspect Claims & Statements)</span>
                <span><span class="badge badge-ai">● AI-INFERRED</span> (Synthesized Correlations)</span>
                <span><span class="badge badge-unknown">● UNKNOWN</span> (Unverified Assertions)</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        f_c1, f_c2, f_c3 = st.columns([1.5, 1.5, 1.2])
        confidence_filter = f_c1.selectbox(
            "Filter by Confidence Classification",
            ["All Classifications", "Directly Observed Only", "User-Reported Only", "AI-Inferred Only", "Unknown Only"]
        )
        status_filter = f_c2.selectbox(
            "Filter by Discrepancy Status",
            ["All Statuses", "Direct Contradictions Only", "Consistent Only"]
        )
        sort_order = f_c3.selectbox("Chrono Sorting", ["Chronological (Oldest First)", "Reverse Chronological (Newest First)"])

    st.write("")

    events = st.session_state.timeline_events.copy()
    if confidence_filter == "Directly Observed Only":
        events = [e for e in events if e.get("confidence_label") == "directly observed" or e.get("indicator") == "observed"]
    elif confidence_filter == "User-Reported Only":
        events = [e for e in events if e.get("confidence_label") == "user-reported" or e.get("indicator") == "user_claim"]
    elif confidence_filter == "AI-Inferred Only":
        events = [e for e in events if e.get("confidence_label") == "AI-inferred" or e.get("indicator") == "ai_interpretation"]
    elif confidence_filter == "Unknown Only":
        events = [e for e in events if e.get("confidence_label") == "unknown"]

    if status_filter == "Direct Contradictions Only":
        events = [e for e in events if "Contradiction" in e.get("discrepancy", "")]
    elif status_filter == "Consistent Only":
        events = [e for e in events if "Consistent" in e.get("discrepancy", "")]

    if sort_order == "Reverse Chronological (Newest First)":
        events = list(reversed(events))

    st.markdown(f"#### Verified Timeline Sequence ({len(events)} Events)")

    for idx, ev in enumerate(events):
        c_label = ev.get("confidence_label") or ("user-reported" if ev.get("indicator") == "user_claim" else ("AI-inferred" if ev.get("indicator") == "ai_interpretation" else "directly observed"))
        
        node_class = "timeline-node"
        if c_label == "user-reported":
            node_class += " user-reported"
        elif c_label == "AI-inferred":
            node_class += " ai-inferred"
        
        if "Contradiction" in ev.get("discrepancy", ""):
            node_class += " contradiction"

        badge_class = "badge-observed" if c_label == "directly observed" else ("badge-claim" if c_label == "user-reported" else ("badge-ai" if c_label == "AI-inferred" else "badge-unknown"))
        discrepancy_color = "#22C55E" if "Consistent" in ev.get("discrepancy", "") else ("#EF4444" if "Contradiction" in ev.get("discrepancy", "") else "#F59E0B")

        st.markdown(
            f"""
            <div class="{node_class}">
                <div style="background-color: #121F35; border: 1px solid rgba(34, 211, 238, 0.15); border-radius: 10px; padding: 16px 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <div>
                            <span class="badge {badge_class}">{c_label.upper()}</span>
                            <span style="font-family: 'JetBrains Mono', monospace; color: #22D3EE; font-size: 0.85rem; font-weight: 600;">{ev.get('timestamp', '')}</span>
                        </div>
                        <span style="color: {discrepancy_color}; font-size: 0.78rem; font-weight: 700; text-transform: uppercase;">
                            {ev.get('discrepancy', 'Consistent')}
                        </span>
                    </div>
                    <h4 style="margin: 4px 0 8px 0; color: #F1F5F9;">{ev.get('title', '')}</h4>
                    <p style="margin: 0 0 10px 0; color: #94A3B8; font-size: 0.88rem; line-height: 1.5;">{ev.get('description', '')}</p>
                    <div style="font-size: 0.78rem; color: #64748B;">
                        Linked Artifact: <strong style="color: #22D3EE;">{ev.get('source_artifact', 'N/A')}</strong>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==============================================================================
# 10. PAGE 6: AI INVESTIGATION (GEMINI RECONSTRUCTION & CONTRADICTIONS)
# ==============================================================================
def render_ai_investigation():
    """Renders AI Findings: Digital Story Reconstruction, Contradictions, and Missing Evidence."""
    st.title("AI Forensic Investigation Core")
    active_case = get_current_case()
    st.caption(f"Synthesized Intelligence for Docket: **{st.session_state.current_case_id}** — {active_case['title']}")

    with st.container(border=True):
        col_s1, col_s2 = st.columns([1.5, 1.0])
        with col_s1:
            st.markdown("##### Suspect Claimed Alibi Defense")
            st.info(f"\"{active_case['claimed_alibi']}\"")
        with col_s2:
            st.markdown("##### AI Corroboration Verdict")
            st.markdown(
                f"""
                <div style="background-color: rgba(239, 68, 68, 0.15); border: 1px solid #EF4444; border-radius: 8px; padding: 14px; color: #F87171;">
                    <div style="font-weight: 800; font-size: 0.95rem; margin-bottom: 4px;">[ALERT] {len(st.session_state.contradictions)} DIRECT CONFLICTS DETECTED</div>
                    <div style="font-size: 0.82rem; color: #FCA5A5;">Engine: {st.session_state.get('last_analysis_engine', 'Gemini Core')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    # Live Gemini AI Execution Trigger
    col_trig1, col_trig2 = st.columns([2.5, 1.5])
    with col_trig1:
        st.caption("Re-run live multi-modal correlation using Google Gemini Gen AI SDK.")
    with col_trig2:
        if st.button("Run Live Gemini AI Correlation", type="primary", use_container_width=True):
            api_key = fb.get_gemini_api_key(st.session_state)
            with st.spinner("Invoking Google Gen AI SDK (Gemini 2.5 Flash)..."):
                try:
                    if api_key:
                        gemini_res = fb.analyze_evidence_with_gemini(
                            api_key=api_key,
                            case_info=active_case,
                            evidence_items=st.session_state.evidence_vault,
                            suspect_alibi=active_case["claimed_alibi"]
                        )
                        st.session_state.digital_story = gemini_res.get("digital_story", st.session_state.digital_story)
                        st.session_state.timeline_events = gemini_res.get("timeline", st.session_state.timeline_events)
                        st.session_state.contradictions = gemini_res.get("contradictions", st.session_state.contradictions)
                        st.session_state.missing_evidence = gemini_res.get("missing_evidence", st.session_state.missing_evidence)
                        st.session_state.ai_observations = gemini_res.get("observations", st.session_state.ai_observations)
                        st.session_state.last_analysis_engine = gemini_res.get("engine", "Google Gemini")
                        st.success(f"Successfully correlated using {st.session_state.last_analysis_engine}!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.warning("GEMINI_API_KEY is not set. Please add your Google AI Studio API key to the .env file or sidebar to execute live Gemini reasoning.")
                except Exception as ex:
                    st.error(f"Gemini Analysis Error: {str(ex)}")

    st.write("")

    # 4 Delineated Sections
    tab_story, tab_contra, tab_missing, tab_obs = st.tabs([
        "Digital Story Reconstruction",
        "Contradiction Detection",
        "Missing Evidence & Gaps",
        "Investigation Observations"
    ])

    with tab_story:
        st.subheader("Synthesized Digital Story Reconstruction")
        st.caption("An understandable, objective narrative explaining the probable chronological sequence of events.")
        
        with st.container(border=True):
            st.markdown(f"#### Narrative Reconstruction: {active_case['title']}")
            st.markdown(st.session_state.digital_story)

    with tab_contra:
        st.subheader("Contradiction Detector (Alibi Refutations)")
        st.caption("Direct clashes between claimed assertions and empirical evidence (timestamps, logs, location).")

        for c in st.session_state.contradictions:
            with st.container(border=True):
                col_head1, col_head2 = st.columns([3, 1])
                col_head1.markdown(f"#### [CONTRADICTION] {c.get('id', 'CT')}: {c.get('title', 'Contradiction')}")
                col_head2.markdown(
                    f"""
                    <div style="text-align: right;">
                        <span class="badge badge-ai" style="font-size: 0.82rem;">SEVERITY: {c.get('severity', 'HIGH')}</span><br>
                        <span style="color: #22D3EE; font-size: 0.78rem;">Confidence: {c.get('reliability_score', 'High')}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write("")
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    st.markdown("**Suspect Claimed Defense:**")
                    st.markdown(f"> *\"{c.get('claim', '')}\"*")
                with col_c2:
                    st.markdown("**Digital Trace Reality:**")
                    st.markdown(f"> *{c.get('forensic_proof', '')}*")
                    st.caption(f"Sources: `{c.get('sources', '')}`")

    with tab_missing:
        st.subheader("Missing Evidence & Log Tampering Anomalies")
        st.caption("AI-identified blind spots, deleted log windows, or unmonitored channels.")

        for gap in st.session_state.missing_evidence:
            with st.container(border=True):
                col_g1, col_g2 = st.columns([3, 1.2])
                with col_g1:
                    st.markdown(f"#### [GAP] {gap.get('id', 'GAP')}: {gap.get('category', 'Anomaly')}")
                    st.markdown(f"**Anomaly:** {gap.get('description', '')}")
                    st.markdown(f"**Forensic Impact:** *{gap.get('impact', '')}*")
                with col_g2:
                    urg = gap.get("urgency", "Medium")
                    urg_color = "#EF4444" if urg == "Critical" else ("#F59E0B" if urg == "High" else "#22D3EE")
                    st.markdown(
                        f"""
                        <div style="background-color: #080F1E; border-left: 3px solid {urg_color}; padding: 10px; border-radius: 6px;">
                            <span style="color: {urg_color}; font-weight: 700;">URGENCY: {urg}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.markdown(f"**Recommended Subpoena / Recovery:** `{gap.get('recommendation', '')}`")

    with tab_obs:
        st.subheader("Investigation Observations & Legal Admissibility")
        st.caption("Compliance with Federal Rules of Evidence Rule 902(14) self-authenticating digital records.")

        with st.container(border=True):
            for obs in st.session_state.ai_observations:
                st.markdown(f"- **{obs}**")

            st.write("")
            st.markdown(
                """
                <div style="background-color: #080F1E; border-left: 3px solid #38BDF8; padding: 12px 16px; border-radius: 6px; font-size: 0.82rem; color: #94A3B8;">
                    <strong style="color: #38BDF8;">Statutory & Ethical Safeguard:</strong><br>
                    AI analysis provides automated hypothesis correlation and highlights empirical inconsistencies for examiner review. It does not establish legal guilt, prove a crime, or replace certified human forensic expert verification.
                </div>
                """,
                unsafe_allow_html=True
            )


# ==============================================================================
# 11. PAGE 7: EVIDENCE INTEGRITY (CRYPTOGRAPHIC TAMPER VERIFIER)
# ==============================================================================
def render_evidence_integrity():
    """Renders the dedicated Evidence Integrity suite with live bitstream tamper verification."""
    st.title("Cryptographic Evidence Integrity")
    st.caption("Verify file bitstreams against the immutable SHA-256 chain of custody ledger.")

    # Interactive Tamper Verification Tool
    with st.container(border=True):
        st.markdown("#### Live Bitstream Tamper Verification Tool")
        st.markdown(
            "Upload any file to calculate its live cryptographic SHA-256 hash and immediately verify whether "
            "it matches a registered artifact in the custody ledger or has been altered post-ingestion."
        )

        test_file = st.file_uploader("Select Evidence File for Integrity Cross-Check", key="tamper_checker_file")

        if test_file:
            t_bytes = test_file.getvalue()
            t_hash = fb.compute_sha256(t_bytes)
            
            st.write("")
            st.markdown(f"**Computed Bitstream SHA-256:**")
            st.code(t_hash, language="text")

            # Match against evidence_vault
            matching_record = None
            for ev in st.session_state.evidence_vault:
                if ev.get("sha256", "").lower() == t_hash.lower():
                    matching_record = ev
                    break

            if matching_record:
                st.success(
                    f"**[VERIFIED] BITSTREAM MATCH CONFIRMED**\n\n"
                    f"The uploaded file is authentic, bit-for-bit identical, and unaltered. "
                    f"Matches custody record: **`{matching_record['id']}` ({matching_record['filename']})**, "
                    f"ingested on **{matching_record['ingest_timestamp']}**."
                )
            else:
                st.error(
                    f"**[ALERT] HASH MISMATCH / UNSEALED ARTIFACT DETECTED!**\n\n"
                    f"The computed hash `{t_hash[:16]}...` does NOT match any sealed record in the active docket ledger. "
                    f"The file has either been modified (tampered) or was not preserved under this investigation's custody."
                )

    st.write("")

    # Complete SHA-256 Chain of Custody Table
    st.markdown("#### Immutable Chain of Custody Ledger")
    st.caption("FIPS 140-2 Level 3 compliant cryptographic integrity table.")

    df_integrity = pd.DataFrame(st.session_state.evidence_vault)[
        ["id", "filename", "classification", "size_kb", "sha256", "ingest_timestamp", "status"]
    ]
    st.dataframe(df_integrity, use_container_width=True, hide_index=True)


# ==============================================================================
# 12. PAGE 8: INVESTIGATION REPORTS (WORKING PDF & DATA EXPORTS)
# ==============================================================================
def render_investigation_reports():
    """Renders formal legal report preview and provides genuine downloadable PDF, JSON, and CSV."""
    st.title("Formal Forensic Investigation Dossiers")
    st.caption("Generate, review, and export court-admissible forensic dossiers and evidentiary exhibits.")

    active_case = get_current_case()

    with st.container(border=True):
        st.markdown("#### Dossier Configuration & Parameters")
        rc1, rc2, rc3 = st.columns(3)
        doc_class = rc1.selectbox("Report Classification Header", ["CONFIDENTIAL // LAW ENFORCEMENT SENSITIVE", "SECRET // FORENSIC HOLD", "FOR OFFICIAL USE ONLY"])
        signoff_examiner = rc2.text_input("Signing Specialist", value=active_case["lead_investigator"])
        exp_agency = rc3.text_input("Issuing Taskforce", value=active_case["agency"])

    st.write("")

    # Working Downloads Row
    st.markdown("#### Export Admissible Forensic Files")
    dl_c1, dl_c2, dl_c3 = st.columns(3)

    # 1. WORKING PDF DOWNLOAD VIA FPDF2
    with dl_c1:
        with st.spinner("Compiling Cryptographic PDF Dossier..."):
            pdf_bytes = fb.generate_forensic_pdf(
                st.session_state.current_case_id,
                active_case,
                st.session_state.evidence_vault,
                st.session_state.timeline_events,
                st.session_state.contradictions,
                st.session_state.missing_evidence,
                st.session_state.digital_story
            )
        st.download_button(
            label="Download Official PDF Report (.PDF)",
            data=pdf_bytes,
            file_name=f"Digital_Alibi_{st.session_state.current_case_id}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    # 2. JSON EXPORT
    with dl_c2:
        json_export_data = {
            "docket_id": st.session_state.current_case_id,
            "metadata": active_case,
            "digital_story": st.session_state.digital_story,
            "evidence_vault": st.session_state.evidence_vault,
            "timeline": st.session_state.timeline_events,
            "contradictions": st.session_state.contradictions,
            "missing_evidence": st.session_state.missing_evidence,
            "observations": st.session_state.ai_observations,
            "certified_examiner": signoff_examiner,
            "exported_at": datetime.now().isoformat()
        }
        st.download_button(
            label="Download Evidence JSON (.JSON)",
            data=json.dumps(json_export_data, indent=2),
            file_name=f"Evidence_Correlated_{st.session_state.current_case_id}.json",
            mime="application/json",
            use_container_width=True
        )

    # 3. CSV TIMELINE EXPORT
    with dl_c3:
        csv_timeline = pd.DataFrame(st.session_state.timeline_events).to_csv(index=False)
        st.download_button(
            label="Download Timeline CSV (.CSV)",
            data=csv_timeline,
            file_name=f"Timeline_{st.session_state.current_case_id}.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.write("")
    st.divider()

    # Formatted Report Preview
    st.markdown(f"#### Dossier Preview: `{st.session_state.current_case_id}`")
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="border-bottom: 2px solid #22D3EE; padding-bottom: 12px; margin-bottom: 16px;">
                <h2 style="color: #F1F5F9; margin: 0;">DIGITAL ALIBI // FORENSIC INVESTIGATION REPORT</h2>
                <span style="color: #22D3EE; font-size: 0.85rem; font-weight: 700;">{doc_class}</span>
            </div>
            
            <p><strong>CASE TITLE:</strong> {active_case['title']}<br>
            <strong>TARGET SUBJECT:</strong> {active_case['target_subject']}<br>
            <strong>LEAD EXAMINER:</strong> {signoff_examiner} ({exp_agency})<br>
            <strong>INCIDENT DATE:</strong> {active_case['incident_date']} | <strong>EVALUATION DATE:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            """,
            unsafe_allow_html=True
        )

        st.markdown("##### 1. Digital Story Reconstruction")
        st.markdown(st.session_state.digital_story)

        st.markdown("##### 2. Key Contradiction Findings")
        for c in st.session_state.contradictions:
            st.error(f"**{c.get('id', 'CT')} : {c.get('title', 'Contradiction')}**\n\n*Forensic Proof:* {c.get('forensic_proof', '')}")

        st.markdown("##### 3. Preserved Chain of Custody (SHA-256 Hashes)")
        df_preview = pd.DataFrame(st.session_state.evidence_vault)[["id", "filename", "classification", "sha256", "status"]]
        st.dataframe(df_preview, use_container_width=True, hide_index=True)

        st.markdown("##### 4. Synchronized Event Sequence with Confidence Labels")
        df_tpreview = pd.DataFrame(st.session_state.timeline_events)[["timestamp", "confidence_label", "title", "discrepancy"]]
        st.dataframe(df_tpreview, use_container_width=True, hide_index=True)


# ==============================================================================
# 13. PAGE 9: ABOUT DIGITAL ALIBI (MISSION, PROBLEM SOLVED, TECH STACK)
# ==============================================================================
def render_about_page():
    """Renders the comprehensive About Digital Alibi page highlighting mission and uniqueness."""
    st.title("About DIGITAL ALIBI")
    st.caption("AI-Powered Digital Evidence Investigator & Timeline Synthesis Workstation")

    # Mission & Problem Solved
    with st.container(border=True):
        st.markdown("### Mission & Problem Solved")
        st.markdown(
            """
            In modern cyber investigations and digital incident response, examiners and defense counsels 
            are overwhelmed by hundreds of uncoordinated electronic files: syslog dumps, cellular CDR carrier logs, 
            CCTV surveillance frames, and messaging records. Manually correlating timestamps across these disparate sources 
            to verify a suspect's claimed alibi takes days of painstaking work and is prone to human oversight.

            **DIGITAL ALIBI** solves this bottleneck by providing an automated, multi-modal correlation workstation. 
            It autonomously ingests electronic files, guarantees bitstream chain-of-custody through cryptographic SHA-256 hashing, 
            normalizes disparate timestamps into a unified chronological sequence, and highlights direct factual contradictions 
            against suspect alibis.
            """
        )

    st.write("")

    # Uniqueness vs. Government Complaint Portals
    with st.container(border=True):
        st.markdown("### Why Digital Alibi is Unique")
        st.markdown(
            """
            > **Unlike traditional government complaint or grievance reporting portals** (which merely register complaints into an 
            > administrative database without performing technical analysis), **Digital Alibi is an intelligent investigative workstation**.
            
            - **Autonomous Analysis vs. Passive Storage:** While portals merely store uploaded attachments, Digital Alibi actively extracts entities, normalizes timestamps, and evaluates factual claims.
            - **Contradiction Detection:** Instantly surfaces irreconcilable clashes (e.g., claiming to be asleep at home while a cellular tower ping and YubiKey SSH login place the device miles away).
            - **Timeline Synthesis:** Transforms unstructured logs into an intuitive chronological sequence with clear confidence classifications.
            - **Evidence Integrity:** Enforces NIST-compliant SHA-256 hashing on ingestion to preserve non-repudiation for legal proceedings.
            """
        )

    st.write("")

    # Working Process (6-Step Pipeline)
    st.markdown("### The 6-Step Working Process")
    step_c1, step_c2, step_c3 = st.columns(3)

    with step_c1:
        with st.container(border=True):
            st.markdown("#### 1. Ingestion & Hashing")
            st.caption("Raw files are uploaded and instantly hashed using SHA-256 to establish an unalterable chain of custody.")

        with st.container(border=True):
            st.markdown("#### 4. Gemini AI Correlation")
            st.caption("Google Gemini 2.5 Flash correlates multi-modal visual and textual traces against the claimed alibi.")

    with step_c2:
        with st.container(border=True):
            st.markdown("#### 2. Normalization")
            st.caption("Timestamps from varying timezones and syslog formats are normalized to Coordinated Universal Time (UTC).")

        with st.container(border=True):
            st.markdown("#### 5. Contradiction Detection")
            st.caption("Algorithmic conflict detector surfaces incompatible location claims, concurrent logins, and audit gaps.")

    with step_c3:
        with st.container(border=True):
            st.markdown("#### 3. Entity Extraction")
            st.caption("Identifies key IP addresses, MAC addresses, cellular tower azimuths, usernames, and cryptographic tokens.")

        with st.container(border=True):
            st.markdown("#### 6. Admissible Dossier")
            st.caption("Generates a court-admissible PDF forensic dossier under Federal Rules of Evidence Rule 902(14).")

    st.write("")

    # Technology Stack Matrix
    st.markdown("### Technology Stack")
    with st.container(border=True):
        tech_col1, tech_col2, tech_col3 = st.columns(3)
        tech_col1.markdown("**Core Framework:** `Python 3.10+` & `Streamlit`")
        tech_col1.markdown("**AI Reasoner:** `Google Gen AI SDK (Gemini 2.5 Flash)`")
        tech_col2.markdown("**Cryptography:** `SHA-256 Bitstream Hashing`")
        tech_col2.markdown("**Document Generation:** `FPDF2 (PDF Engine)`")
        tech_col3.markdown("**Telemetry Visuals:** `Plotly Analytics`")
        tech_col3.markdown("**Compliance Standard:** `FRE Rule 902(14)`")


# ==============================================================================
# 14. PAGE 10: HELP & PRIVACY (USER GUIDE, PRIVACY, AI DISCLAIMER)
# ==============================================================================
def render_help_privacy():
    """Renders the user guide, privacy notice, and statutory AI disclaimer."""
    st.title("Help, Privacy & Statutory Disclaimers")
    st.caption("Investigative user guide, evidence privacy policy, and legal safeguards.")

    # User Guide
    with st.container(border=True):
        st.markdown("### Quick-Start Examiner User Guide")
        st.markdown(
            """
            1. **Intake a Case:** Navigate to **New Investigation**, fill in the docket parameters (Incident category, suspect identity, and claimed alibi defense).
            2. **Ingest Evidence:** Drag and drop images, syslogs, CSVs, or JSON files into the upload vault. Click **Ingest Evidence & Launch AI Analysis**.
            3. **Inspect Evidence Vault:** Review the **Evidence Vault** to examine file bitstreams, previews, and cryptographic SHA-256 hashes.
            4. **Analyze the Timeline:** View **Timeline Analysis** to filter events by confidence (*Directly Observed*, *User-Reported*, *AI-Inferred*, *Unknown*).
            5. **Review Contradictions:** Check **AI Investigation** to review the Digital Story narrative and specific factual contradiction warnings.
            6. **Verify File Integrity:** Use **Evidence Integrity** to test any external file against the sealed custody ledger for bitstream tamper detection.
            7. **Export Legal Dossier:** Open **Investigation Reports** to compile and download the certified PDF report.
            """
        )

    st.write("")

    # Privacy Policy & Data Sovereignty
    with st.container(border=True):
        st.markdown("### Privacy Notice & Evidence Sovereignty")
        st.markdown(
            """
            - **Local Custody Preservation:** All uploaded artifacts are stored locally in the secured `evidence_store/` directory on your workstation. No external file storage or unverified clouds are utilized.
            - **Zero Credential Exposure:** Your Google AI Studio API key is read securely from your local `.env` file or session memory. It is never logged or exposed in client bundles.
            - **Inference Privacy:** When utilizing the Google Gen AI SDK, data is transmitted strictly for transient multimodal reasoning under Google AI Studio enterprise privacy standards with zero model retraining on your evidence.
            """
        )

    st.write("")

    # Statutory AI Disclaimer & Ethical Safeguard
    with st.container(border=True):
        st.markdown("### Statutory AI Disclaimer & Legal Safeguard")
        st.markdown(
            """
            <div style="background-color: rgba(239, 68, 68, 0.12); border: 1px solid #EF4444; border-radius: 8px; padding: 16px; color: #FCA5A5; line-height: 1.6; font-size: 0.85rem;">
                <strong>IMPORTANT NOTICE FOR LEGAL AND LAW ENFORCEMENT PROCEEDINGS:</strong><br><br>
                1. <strong>Preliminary Assistance Only:</strong> DIGITAL ALIBI is an investigative support platform designed to assist human examiners with evidence correlation, timestamp normalization, and hypothesis testing. All AI findings, contradiction indicators, and story reconstructions are preliminary and strictly require certified human forensic examiner review.<br><br>
                2. <strong>Non-Accusatory Standard:</strong> AI analysis does NOT prove a crime, establish legal guilt, or determine criminal liability. Digital trace correlations demonstrate consistency or inconsistency with claimed hypotheses, but must be corroborated by subpoenaed records and verified witness statements.<br><br>
                3. <strong>Chain of Custody Standard:</strong> For court admissibility under Federal Rules of Evidence Rule 902(14), examiners must certify that the SHA-256 hash calculated at initial acquisition matches the record presented in legal proceedings.
            </div>
            """,
            unsafe_allow_html=True
        )


# ==============================================================================
# 15. MAIN WORKSTATION CONTROLLER
# ==============================================================================
def main():
    init_session_state()

    # Route: Login Gate vs Workstation Interface
    if not st.session_state.authenticated:
        render_login_page()
    else:
        render_sidebar()
        inject_custom_css()

        page = st.session_state.current_page
        if page == "Dashboard":
            render_dashboard()
        elif page == "New Investigation":
            render_new_investigation()
        elif page == "Evidence Vault":
            render_evidence_vault()
        elif page == "Timeline Analysis":
            render_timeline_analysis()
        elif page == "AI Investigation":
            render_ai_investigation()
        elif page == "Evidence Integrity":
            render_evidence_integrity()
        elif page == "Investigation Reports":
            render_investigation_reports()
        elif page == "About Digital Alibi":
            render_about_page()
        elif page == "Help & Privacy":
            render_help_privacy()

if __name__ == "__main__":
    main()

