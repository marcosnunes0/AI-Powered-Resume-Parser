# 🚀 AI Powered Resume Parser

> A lightweight web app that leverages free AI (Llama 3.3 via Grok API) to score, summarize and critique PDF resumes based on a selected job vacancy.

---

## ✨ Core Features
• **Resume Scoring** – AI‑driven ranking by job‑fit.  
• **Summary Generation** – Concise overview of each CV.  
• **Descriptive Critique** – Highlights strengths, misalignments & improvement areas.  
• **Downloadable CVs** – One‑click PDF retrieval.

All powered by a Streamlit front‑end, TinyDB storage, Google Drive integration, and LangChain–Grok AI.

---

## 🛠️ Tech Stack
![Python](https://img.shields.io/badge/Python->=3.11-05122A?logo=python&style=flat) ![Streamlit](https://img.shields.io/badge/Streamlit-UI-05122A?logo=streamlit&style=flat) ![TinyDB](https://img.shields.io/badge/TinyDB-NoSQL-05122A?logo=approov&style=flat) ![Google Drive](https://img.shields.io/badge/Google_Drive-API-05122A?logo=googledrive&style=flat) ![PaimuPDF](https://img.shields.io/badge/PaimuPDF-PDF_Parsing-05122A?style=flat)
![Llama3](https://img.shields.io/badge/Llama_3.3-70B-05122A?style=flat) ![GrokAPI](https://img.shields.io/badge/Grok_API-LangChain-05122A?style=flat)

## 💻 Architecture & Flow

```
┌──────────────────┐      ┌───────────────┐      ┌──────────────┐
│ Google Drive API │ ──→  │   Helper      │ ──→  │    AI Layer  │
│  (download CVs)  │      │ (read_pdf,    │      │ (ChatGrok →  │
└──────────────────┘      │  TinyDB)      │      │  Llama 3.3)  │
                          └───────────────┘      └──────────────┘
                                     ↓                     ↓
                                ┌──────────┐          ┌───────────┐
                                │ Database │          │ Streamlit │
                                │ (TinyDB) │          │  Front‑end│
                                └──────────┘          └───────────┘
```

## 📂 Project Structure

```bash
ai-powered-resume-parser/
├── AI-Powered-Resume-Parser/
│   ├── drive/                  # Google Drive integration
|   |   ├── authenticate.py     # OAuth2 setup for Drive API
|   |   └── download_cv.py      # Downloads resumes from Drive
│   ├── models/                 # Pydantic schemas (job, resum, analysis, file)
│   ├── ai.py                   # Groq API integration
│   ├── ai_analysis.py          # CV processing pipeline
│   ├── app.py                  # Streamlit UI
│   ├── create_job.py           # Vacancy creation
│   ├── database.py             # TinyDB operations
│   └── helper.py               # PDF utilities
├── CVs/                        # Downloaded PDF CVs at runtime
├── db.json                     # Database file
├── requirements.txt            # Dependencies
├── LICENSE
└── README.md
```

## ⚙️ Setup & Installation

**Prerequisites**

- Python 3.11+

- Groq API Key (free account)

**Installation Steps**

**1. Clone the repository:**

```bash
git clone https://github.com/marcosnunes0/ai-powered-resume-parser.git
cd ai-powered-resume-parser
```

**2. Create and activate virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables:**

```bash
echo "GROQ_API_KEY=your_api_key_here" > .env
```

**5. Set up Google Drive integration:**

- Create a Google service account and enable the Drive API.

- Download ```credentials.json``` and place it in the project root.

- Run authentication script:

```bash
python AI-Powered-Resume-Parser/drive/authenticate.py
```

## ▶️ Usage

<details> <summary>1. Create Job Vacancy</summary>

```bash
python AI-Powered-Resume-Parser/create_job.py
```

Generates the vacancy in the ```db.jason``` database

Obs: Before running the script to actually create the job, it is necessary to change the desired characteristics of the job in the ```create_job.py``` file.
</details>

<details> <summary>2. Authenticate & Download CVs</summary>

**Option A: From Google Drive**

```bash
python AI-Powered-Resume-Parser/drive/authenticate.py
python AI-Powered-Resume-Parser/drive/download_cv.py
```

**Option B: Manual Placement**

Place PDF resumes in the CVs/ directory

Obs: Both option A procedure and option B procedure will populate the CVs/ folder with applicant PDFs.
</details>

<details> <summary>3. Run AI Analysis</summary>

```bash
python AI-Powered-Resume-Parser/ai_analysis.py
```

Generates summaries, scores, critiques and stores results in ```db.json```.
</details>

<details> <summary>4. Launch Streamlit App</summary>

```bash
streamlit run ./AI-Powered-Resume-Parser/app.py
```

- Open your browser at http://localhost:8501

- Select a job vacancy

- Select the candidates from the table whose summaries and reviews you want to see

- Download original resums with one click
</details>

## 🤝 Contributing

Contributions and feedback are welcome!

1. Fork the repository

2. Create a feature branch (```git checkout -b feature/YourFeature```)

3. Commit your changes (```git commit -m "Add feature"```)

4. Push to your branch (```git push origin feature/YourFeature```)

5. Open a Pull Request

## ⚠️ Known Limitations

- Requires consistent PDF formatting for optimal parsing

- Accuracy depends on Groq API performance

- Google Drive authentication needed for cloud integration

- Score variability with complex/creative resumes

## 📄 License

Released under the [MIT License](https://github.com/marcosnunes0/AI-Powered-Resume-Parser/blob/main/LICENSE).