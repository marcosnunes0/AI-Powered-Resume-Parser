# 🚀 AI Powered Resume Parser

> A lightweight web app that leverages free AI (Llama 3.1 via Grok API) to score, summarize and critique PDF resumes based on a selected job vacancy.

---

## ✨ Core Features
• **Resume Scoring** – AI‑driven ranking by job‑fit.  
• **Summary Generation** – Concise overview of each CV.  
• **Descriptive Critique** – Highlights strengths, misalignments & improvement areas.  
• **Downloadable CVs** – One‑click PDF retrieval.

---

## 🛠️ Tech Stack
![Python](https://img.shields.io/badge/Python->=3.11-05122A?logo=python&style=flat) ![Streamlit](https://img.shields.io/badge/Streamlit-UI-05122A?logo=streamlit&style=flat) ![TinyDB](https://img.shields.io/badge/TinyDB-NoSQL-05122A?logo=approov&style=flat) ![Google Drive](https://img.shields.io/badge/Google_Drive-API-05122A?logo=googledrive&style=flat) ![PaimuPDF](https://img.shields.io/badge/PaimuPDF-PDF_Parsing-05122A?style=flat)
![Llama3](https://img.shields.io/badge/Llama_3.1-70B-05122A?style=flat) ![GrokAPI](https://img.shields.io/badge/Grok_API-LangChain-05122A?style=flat)

feat: Initial project structure and core functionality

This commit introduces the initial structure and core functionality of the AI-Powered Resume Parser. 
 
The project is organized as follows: 
 
- AI-Powered-Resume-Parser/drive/: Contains scripts for Google Drive integration.

- authenticate.py: Handles OAuth 2.0 authentication with the Google Drive API, creating and refreshing `token.json`.

- download_cv.py: Downloads summaries from a specified Google Drive folder into the `CVs/` directory. 

- AI-Powered-Resume-Parser/: Intended for the main resume analysis application (currently empty). 

- CVs/: a directory that receives the CVs downloaded via Google Drive API. 

- requirements.txt: Lists all Python dependencies for the project.