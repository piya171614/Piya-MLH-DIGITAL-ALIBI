# 🛡️ DIGITAL ALIBI: AI Digital Evidence Investigator

> *"Every Digital Trace Tells a Story."*

**DIGITAL ALIBI** is an autonomous cyber-forensics platform built with **Python Streamlit** and the official **Google Gen AI Python SDK (`google-genai`)**. It correlates multi-source digital evidence (system syslogs, cellular tower CDR dumps, surveillance CCTV frames, encrypted chat transcripts, Wi-Fi RADIUS sessions) to reconstruct verified chronological timelines, detect investigative blind spots, and identify factual contradictions against suspect alibis.

---

## 🧭 Complete Workstation Navigation Modules

| Module | Icon | Description |
| :--- | :---: | :--- |
| **Dashboard** | 📊 | Operational command center, dynamic telemetry statistics cards (investigations, evidence files, milestones, contradictions, data volume), Plotly charts, and recent activity. |
| **New Investigation** | 📁 | Case intake form with multi-file drag-and-drop vault supporting images, logs, and CSVs with real-time SHA-256 calculation. |
| **Evidence Vault** | 📦 | Preserved evidence cards with SHA-256 hashes, bitstream previews for images and text logs, and classification filters. |
| **Timeline Analysis** | ⏳ | Chronological interactive vertical timeline with confidence labels (`Directly Observed`, `User-Reported`, `AI-Inferred`, `Unknown`). |
| **AI Investigation** | 🧠 | Gemini-powered Digital Story Reconstruction, Contradiction Matrix, and Missing Evidence discovery. |
| **Evidence Integrity** | 🔒 | Dedicated cryptographic tamper verification tool allowing examiners to upload any file to verify bitstream authenticity against the sealed ledger. |
| **Investigation Reports** | 📑 | Court-admissible report preview with working PDF, JSON, and CSV exports. |
| **About Digital Alibi** | ℹ️ | Project mission, objectives, uniqueness vs. traditional government complaint portals, working process, and technology stack. |
| **Help & Privacy** | 🛡️ | Step-by-step examiner user guide, evidence data privacy policy, and statutory AI disclaimer. |
| **Logout** | 🚪 | Securely lock the workstation and return to the login portal. |

---

## 🎨 Theme & Cyber-Forensics Workstation Styling

- **Main Background:** `#080F1E` (Dark Navy)
- **Sidebar Surface:** `#0D1729` (Deep Slate)
- **Cards & Containers:** `#121F35` with subtle cyan borders (`rgba(34, 211, 238, 0.15)`)
- **Primary Blue & Electric Cyan:** `#2563EB` & `#22D3EE`
- **Forensic Status Indicators:** `#22C55E` (Verified), `#F59E0B` (User Claim / Warning), `#EF4444` (Contradiction / Danger)
- **Fonts:** `Inter` for clean typography and `JetBrains Mono` for cryptographic checksums and timestamps.

---

## 🚀 Beginner-Friendly Installation & Running Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Set Your Google Gemini API Key
Add your Google AI Studio API key in `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*Note: If no API key is provided, DIGITAL ALIBI automatically engages its built-in Deterministic Forensic Engine so judges and evaluators can explore the entire workflow offline.*

### 4. Run the Application
Launch the Streamlit app:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8503` and click **"⚡ Without Sign In"** to immediately open the full forensics dashboard.

---

## ⚖️ Legal & Ethical Safeguard
*DIGITAL ALIBI is an investigative support platform designed to assist human examiners with multi-source evidence correlation under Federal Rules of Evidence Rule 902(14). AI correlation results identify evidentiary inconsistencies and temporal patterns; they do not establish legal guilt, prove a crime, or replace certified human forensic expert verification.*
