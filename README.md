# 🚀 AI Powered Resume Parser

> An intelligent web application that leverages AI (Llama 3.3 70B via Groq API) to score, summarize and critically analyze PDF resumes against a selected job vacancy all through an intuitive Streamlit interface.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📝 **Job Registration** | Create job vacancies directly from the UI with title, activities, prerequisites, and differentials. |
| ⚙️ **Job Management** | View, edit, and delete existing vacancies with a confirmation step to prevent accidental deletions. |
| 🤖 **AI-Powered Analysis** | Trigger the full CV analysis pipeline from the interface. The AI summarizes, scores and generates a detailed critical opinion for each candidate. |
| 📊 **Interactive Ranking** | Visualize candidate rankings through bar charts and an interactive table with sorting and multi-selection. |
| 📄 **CV Download** | Download the original PDF resume for any selected candidate with one click. |
| 📊 **Export Analysis PDF** | Export a formatted PDF report containing the AI's summary and opinion for each candidate. |
| ☁️ **Google Drive Integration** | Optionally download candidate CVs directly from a Google Drive folder. |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python->=3.11-05122A?logo=python&style=flat) ![Streamlit](https://img.shields.io/badge/Streamlit-UI-05122A?logo=streamlit&style=flat) ![TinyDB](https://img.shields.io/badge/TinyDB-NoSQL-05122A?logo=approov&style=flat) ![Google Drive](https://img.shields.io/badge/Google_Drive-API-05122A?logo=googledrive&style=flat) ![PyMuPDF](https://img.shields.io/badge/PyMuPDF-PDF_Parsing-05122A?style=flat)
![Llama3](https://img.shields.io/badge/Llama_3.3-70B-05122A?style=flat) ![GroqAPI](https://img.shields.io/badge/Groq_API-LangChain-05122A?style=flat)

| Technology | Purpose |
|---|---|
| **Streamlit** | Web interface |
| **LangChain + Groq** | AI integration (model: `llama-3.3-70b-versatile`) |
| **TinyDB** | Lightweight JSON-based NoSQL database (`db.json`) |
| **PyMuPDF (fitz)** | PDF text extraction and PDF report generation |
| **Pydantic** | Data validation and schema modeling |
| **Pandas + AgGrid** | Data manipulation and interactive table rendering |
| **Google Drive API** | Optional cloud-based CV retrieval |

---

## 💻 Architecture & Flow

```
                          ┌─────────────────────────────────────────┐
                          │           Streamlit Interface           │
                          │  ┌──────┬───────────┬────────┬────────┐ │
                          │  │ Home │ Register  │ Manage │Analysis│ │
                          │  │      │   Job     │  Jobs  │        │ │
                          │  └──────┴───────────┴────────┴────────┘ │
                          └──────────────┬──────────────────────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
           ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
           │   Database   │    │  AI Analysis │    │  PDF Export  │
           │   (TinyDB)   │    │  (LangChain  │    │  (PyMuPDF)   │
           │   db.json    │    │  + Groq API) │    │              │
           └──────────────┘    └──────────────┘    └──────────────┘
                                       ▲
                                       │
                               ┌───────────────┐
                               │   Helper      │
                               │  (read_pdf,   │
                               │   extract)    │
                               └───────┬───────┘
                                       ▲
                          ┌────────────┴────────────┐
                          ▼                         ▼
                 ┌──────────────┐          ┌──────────────┐
                 │  Local CVs   │          │ Google Drive │
                 │  (CVs/)      │          │  (download)  │
                 └──────────────┘          └──────────────┘
```

---

## 📂 Project Structure

```bash
ai-powered-resume-parser/
├── CVs/                       # PDF resumes directory (populated at runtime)
├── drive/                     # Google Drive integration
│   ├── authenticate.py        # OAuth2 setup for Drive API
│   └── download_cv.py         # Downloads resumes from Drive
├── models/                    # Pydantic data schemas
│   ├── analysis.py            # Analysis model (name, skills, score, etc.)
│   ├── file.py                # File tracking model
│   ├── job.py                 # Job vacancy model
│   └── resum.py               # Resume summary model
├── ai.py                      # Groq API client (summarize, score, opinion)
├── ai_analysis.py             # CV processing pipeline (run_analysis function)
├── app.py                     # Streamlit application (main UI)
├── database.py                # TinyDB database operations (CRUD)
├── helper.py                  # PDF utilities (read_pdf, generate_analysis_pdf)
├── create_job.py              # Legacy script for manual job creation
├── db.json                    # TinyDB database file
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (API keys)
├── LICENSE                    # MIT License
└── README.md                  # This file
```

---

## ⚙️ Setup & Installation

### Prerequisites

- **Python 3.11+** installed on your system
- A **Groq API Key** (free at [console.groq.com](https://console.groq.com))
- *(Optional)* Google Cloud credentials for Drive integration

### Step-by-Step

**1. Clone the repository:**

```bash
git clone https://github.com/marcosnunes0/AI-Powered-Resume-Parser.git
cd AI-Powered-Resume-Parser
```

**2. Create and activate a virtual environment:**

```bash
python -m venv venv
```

```bash
# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables:**

Create a `.env` file in the project root with the following content:

```env
GROQ_API_KEY=your_groq_api_key_here
FOLDER_ID=your_google_drive_folder_id_here
```

> **Note:** `FOLDER_ID` is only required if you plan to use the Google Drive integration to download CVs automatically. If you will place CVs manually in the `CVs/` folder, you can omit it.

**5. *(Optional)* Set up Google Drive integration:**

If you want to download CVs from Google Drive:

- Create a project in [Google Cloud Console](https://console.cloud.google.com) and enable the **Google Drive API**.
- Create OAuth 2.0 credentials and download the `credentials.json` file.
- Place `credentials.json` in the project root directory.
- Run the authentication script to generate `token.json`:

```bash
python drive/authenticate.py
```

**6. Add candidate CVs:**

Place PDF resume files in the `CVs/` directory, or download them from Google Drive:

```bash
python drive/download_cv.py
```

**7. Launch the application:**

```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## ▶️ Usage Guide

### 🏠 Home

The landing page provides:
- An overview of system statistics (registered jobs, summaries, and analyses).
- A step-by-step guide explaining how the application works.

### 📝 Register Job

1. Navigate to **Register Job** in the sidebar.
2. Fill in the form fields:
   - **Job Title** - Name of the vacancy (e.g., "Senior Software Engineer Vacancy").
   - **Main Activities** - Key responsibilities for the position.
   - **Prerequisites** - Required qualifications and experience.
   - **Differentials** - Desired extra skills and certifications.
3. Click **Register** to save the vacancy to the database.

### ⚙️ Manage Jobs

1. Navigate to **Manage Jobs** in the sidebar.
2. Select a vacancy from the dropdown to view its full details.
3. **Edit**: Expand the "✏️ Edit Job" section, modify the fields, and click **💾 Save Changes**.
4. **Delete**: Click **🗑️ Delete Job**, then confirm the action. All associated analyses and resumes will also be removed.

### 📊 Analysis

1. Navigate to **Analysis** in the sidebar.
2. Select a job vacancy from the dropdown.
3. Click **🤖 Run AI Analysis** to start the AI pipeline. A loading spinner will indicate progress while the AI processes all CVs found in the `CVs/` directory.
4. Once complete, the results are displayed:
   - **Bar chart** ranking all candidates by score.
   - **Interactive table** with sortable columns and multi-selection checkboxes.
5. Select one or more candidates from the table to see:
   - The AI-generated **resume summary**.
   - The AI-generated **critical opinion** (strengths, misalignments, points of attention).
6. For each selected candidate, two download buttons are available:
   - **📄 Download CV** - Downloads the original PDF resume.
   - **📊 Export Analysis** - Downloads a formatted PDF report with the AI analysis.
7. Click **Clear Analysis** to remove all analysis data for the selected vacancy.

---

## 🤝 Contributing

Contributions and feedback are welcome!

1. Fork the repository

2. Create a feature branch (`git checkout -b feature/YourFeature`)

3. Commit your changes (`git commit -m "Add feature"`)

4. Push to your branch (`git push origin feature/YourFeature`)

5. Open a Pull Request

---

## ⚠️ Known Limitations

- Requires consistent PDF formatting for optimal text extraction
- AI accuracy and score consistency depend on Groq API performance and the LLM model
- Google Drive authentication is required for cloud-based CV retrieval
- Score variability may occur with complex or creatively formatted resumes

---

## 📄 License

Released under the [MIT License](https://github.com/marcosnunes0/AI-Powered-Resume-Parser/blob/main/LICENSE).