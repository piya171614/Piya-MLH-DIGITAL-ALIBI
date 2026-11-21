### **Project Modules**

| Module                    | Description                                                                                                                                                                       |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Dashboard**             | Operational command center featuring dynamic statistics cards for investigations, evidence files, milestones, contradictions, and data volume; Plotly charts and recent activity. |
| **New Investigation**     | Case intake form with multi-file drag-and-drop upload support for images, logs, and CSVs, including real-time SHA-256 hash calculation.                                           |
| **Evidence Vault**        | Preserved evidence cards displaying SHA-256 hashes, image and text-log previews, and classification filters.                                                                      |
| **Timeline Analysis**     | Interactive chronological vertical timeline with confidence labels: `Directly Observed`, `User-Reported`, `AI-Inferred`, and `Unknown`.                                           |
| **AI Investigation**      | Gemini-powered Digital Story Reconstruction, Contradiction Matrix, and Missing Evidence Discovery.                                                                                |
| **Evidence Integrity**    | Cryptographic tamper-verification tool that allows examiners to upload files and verify their hashes against the sealed evidence ledger.                                          |
| **Investigation Reports** | Professional investigation report preview with PDF, JSON, and CSV export options.                                                                                                 |
| **About Digital Alibi**   | Project mission, objectives, uniqueness compared with traditional government complaint portals, investigation workflow, and technology stack.                                     |
| **Help & Privacy**        | Step-by-step user guide, evidence privacy policy, and statutory AI disclaimer.                                                                                                    |
| **Logout**                | Securely locks the workstation and returns the user to the login portal.                                                                                                          |
---

##  Theme & Cyber-Forensics Workstation Styling

- **Main Background:** `#080F1E` (Dark Navy)
- **Sidebar Surface:** `#0D1729` (Deep Slate)
- **Cards & Containers:** `#121F35` with subtle cyan borders (`rgba(34, 211, 238, 0.15)`)
- **Primary Blue & Electric Cyan:** `#2563EB` & `#22D3EE`
- **Forensic Status Indicators:** `#22C55E` (Verified), `#F59E0B` (User Claim / Warning), `#EF4444` (Contradiction / Danger)
- **Fonts:** `Inter` for clean typography and `JetBrains Mono` for cryptographic checksums and timestamps.

---

##  Beginner-Friendly Installation & Running Guide

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

##  Legal & Ethical Safeguard
*DIGITAL ALIBI is an investigative support platform designed to assist human examiners with multi-source evidence correlation under Federal Rules of Evidence Rule 902(14). AI correlation results identify evidentiary inconsistencies and temporal patterns; they do not establish legal guilt, prove a crime, or replace certified human forensic expert verification.*
