# AI Resume Screening & Job Recommendation System

An academic AI/ML and Data Science full-stack web application designed to automate resume parsing, evaluate candidate-job compatibility, perform ATS scoring, identify skill gaps, and provide ranked job recommendations using Natural Language Processing (NLP), TF-IDF Vectorization, and Cosine Similarity.

---

## 📌 Project Overview

In traditional recruitment workflows, manual resume evaluation is labor-intensive, slow, and prone to human bias. On the applicant side, candidates frequently face rejection by corporate Applicant Tracking Systems (ATS) without understanding why their profile failed or which skills they lacked.

**The AI Resume Screening & Job Recommendation System** bridges this gap by delivering:
1. **Automated Multi-Format Document Parsing:** Ingests PDF and DOCX files to extract contact info, education, work experience, projects, and technical skills.
2. **Multi-Domain Technical Skill Taxonomy:** Categorizes competencies into Programming Languages, Frameworks, Databases, Cloud & DevOps, Tools, and Concepts.
3. **Academic Multi-Factor Screening Score:** Weighted evaluation across skills (35%), experience (20%), projects (15%), education (10%), completeness (10%), and keyword density (10%).
4. **Corporate ATS Simulation:** Evaluates keyword density, structural formatting, section headers, and qualification alignment.
5. **Interactive Job Description Matcher:** Computes real-time TF-IDF Cosine Similarity and Skill Jaccard indices against any user-pasted job description.
6. **Hybrid Job Recommendation Engine:** Ranks 50+ curated industry roles from a local dataset with personalized "Why Recommended" rationales.
7. **Visual Skill Gap Analysis:** Highlights exact matched vs missing competencies with interactive chart breakdowns.
8. **Section-by-Section Improvement Engine:** Provides actionable tips and an interactive ATS checklist for candidate optimization.
9. **Screening History Tracking:** Persists all analysis snapshots into a local SQLite database for historical review.

---

## 🛠️ Technology Stack

| Layer | Technologies Used | Purpose |
|---|---|---|
| **Frontend** | React 18, Vite, Tailwind CSS, Lucide Icons, Recharts | Modern AI SaaS responsive user interface |
| **Backend** | Python 3.11, Flask, Flask-CORS, Werkzeug | RESTful API microservice architecture |
| **Machine Learning / NLP** | Scikit-learn, NumPy, Regex, Tokenizers | TF-IDF vectorization, Cosine similarity, stopword filtering |
| **Document Parsing** | PyPDF / PyPDF2, pdfplumber, python-docx | Text extraction from PDF & DOCX formats |
| **Database** | SQLite, SQLAlchemy ORM | Local persistence for resumes, jobs, and history |

> **Note:** 100% local processing. **Zero paid API keys or OpenAI tokens required.**

---

## 🧠 AI / ML Workflow & Mathematical Foundations

### 1. Text Preprocessing & Cleaning
Raw document text is normalized:
- URLs, email addresses, and phone numbers are isolated and mapped.
- Domain-specific terms like `C++`, `C#`, `.NET`, and `Node.js` are protected prior to punctuation filtering.
- Text is converted to lowercase, tokenized, and standard English stopwords are removed.

### 2. Term Frequency - Inverse Document Frequency (TF-IDF)
TF-IDF transforms variable-length unstructured text into fixed numerical vector embeddings:

$$\text{TF}(t, d) = \frac{\text{Count of term } t \text{ in document } d}{\text{Total terms in document } d}$$

$$\text{IDF}(t, D) = \log\left(\frac{|D|}{1 + |\{d \in D : t \in d\}|}\right)$$

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

Rare, highly discriminative tech keywords (e.g., *PyTorch*, *FastAPI*, *Kubernetes*) receive high weights, whereas generic words receive lower weights.

### 3. Cosine Similarity
Cosine similarity evaluates the cosine of the angle between candidate vector $\mathbf{A}$ and job description vector $\mathbf{B}$ in multi-dimensional space:

$$\text{Cosine Similarity}(\mathbf{A}, \mathbf{B}) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\|_2 \|\mathbf{B}\|_2} = \frac{\sum_{i=1}^n A_i B_i}{\sqrt{\sum_{i=1}^n A_i^2} \sqrt{\sum_{i=1}^n B_i^2}}$$

### 4. Hybrid Match Formula
To ensure high semantic relevance while guaranteeing core prerequisite fulfillment, a hybrid scoring model is employed:

$$\text{Hybrid Match Score} = (0.55 \times \text{TF-IDF Cosine Similarity}) + (0.45 \times \text{Skill Overlap Ratio})$$

---

## 📂 Project Directory Structure

```
ai-resume-screening-job-recommendation-system/
├── backend/
│   ├── app.py                          # Flask application entry point & factory
│   ├── config.py                       # System configurations, scoring weights, paths
│   ├── database.py                     # SQLAlchemy database initializer
│   ├── requirements.txt                # Python backend dependencies
│   ├── data/
│   │   ├── jobs.csv                    # Dataset containing tech job roles & descriptions
│   │   └── skills_taxonomy.json        # 100+ categorised technical and soft skills
│   ├── models/
│   │   ├── __init__.py
│   │   └── schema.py                   # Resume, Analysis, Job, History SQLAlchemy models
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── tfidf_model.py              # Scikit-learn TF-IDF vectorizer engine
│   │   └── similarity.py               # Cosine similarity & hybrid scoring module
│   ├── services/
│   │   ├── __init__.py
│   │   ├── text_preprocessor.py        # NLP cleaning, tokenization & stopwords
│   │   ├── skill_extractor.py          # Skill dictionary & regex pattern matcher
│   │   ├── resume_parser.py            # PDF & DOCX multi-field entity extractor
│   │   ├── resume_scorer.py            # Weighted academic scoring & ATS auditor
│   │   ├── job_matcher.py              # Single job-to-resume matching engine
│   │   └── recommendation_engine.py    # Multi-job dataset ranking & rationales
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── resume_routes.py            # /api/resume/* endpoints (upload, parse)
│   │   ├── job_routes.py               # /api/jobs/* endpoints (filters, listing, match)
│   │   ├── recommendation_routes.py    # /api/recommendations endpoint
│   │   └── history_routes.py           # /api/history/* endpoints
│   └── uploads/                        # User uploaded resume storage
│
├── frontend/
│   ├── index.html                      # HTML entry with Google Inter font
│   ├── package.json                    # Frontend dependencies
│   ├── vite.config.js                  # Vite bundler configuration
│   ├── tailwind.config.js              # Tailwind custom theme & dark mode config
│   ├── postcss.config.js
│   └── src/
│       ├── main.jsx                    # React entry point
│       ├── App.jsx                     # Layout, theme wrapper & navigation
│       ├── index.css                   # Tailwind styles & glassmorphism utilities
│       ├── context/
│       │   ├── ThemeContext.jsx        # Dark/Light mode state
│       │   └── ResumeContext.jsx       # Candidate resume, analysis & toast state
│       ├── services/
│       │   └── api.js                  # REST API communication layer
│       ├── components/
│       │   ├── Navbar.jsx              # Top header with profile badge & dark mode
│       │   ├── Sidebar.jsx             # Collapsible application navigation
│       │   ├── Footer.jsx              # Project footer & academic attribution
│       │   ├── ScoreGauge.jsx          # Circular animated score gauge
│       │   ├── SkillBadge.jsx          # Matched/Missing/Category skill badge
│       │   ├── LoadingSkeleton.jsx     # Animated AI analysis loader
│       │   ├── EmptyState.jsx          # Empty state container
│       │   └── Toast.jsx               # Floating toast notifications
│       └── pages/
│           ├── LandingPage.jsx         # Hero, features, how it works & tech stack
│           ├── Dashboard.jsx           # Circular score, stats, radar/bar charts, top jobs
│           ├── ResumeUpload.jsx        # Drag-and-drop file upload & raw text input
│           ├── ResumeAnalysis.jsx      # Extracted details, ATS audit, strengths/weaknesses
│           ├── JobMatching.jsx         # Custom job description matching tool
│           ├── JobRecommendations.jsx  # Ranked dataset jobs with search & filters
│           ├── JobDetails.jsx          # Role deep dive with skill gap pie chart
│           ├── ResumeImprovement.jsx   # Section audits & interactive ATS checklist
│           ├── AnalysisHistory.jsx     # SQLite history logs table & reload action
│           └── AboutProject.jsx        # Architecture, ML equations & viva guide
│
├── README.md                           # Complete project guide
├── PROJECT_REPORT.md                   # Formal 18-section academic report
└── VIVA_QUESTIONS.md                   # 30+ Viva Voce questions & detailed answers
```

---

## 🚀 Installation & Running Locally

### Prerequisites
- **Python 3.10+** (Tested on Python 3.11)
- **Node.js 18+** & **npm 9+** (Tested on Node v22.19.0)

---

### Step 1: Clone or Navigate to Project
```bash
cd "d:\Full Stack Projects\ai-resume-screening-jab-recommendation-system"
```

---

### Step 2: Set Up Backend (Python / Flask)

1. Open a terminal in the root directory:
```bash
# Install Python packages
pip install -r backend/requirements.txt

# (Optional) Generate sample PDF and DOCX files for offline testing
python backend/generate_samples.py

# Start Flask backend server (runs on port 5000)
python -m backend.app
```
Backend will start on `http://localhost:5000`. You can verify by opening `http://localhost:5000/api/health` in your browser.

---

### Step 3: Set Up Frontend (React / Vite)

1. Open a separate terminal window:
```bash
cd frontend

# Install npm packages
npm install

# Launch Vite development server
npm run dev
```
Frontend will be accessible at `http://localhost:5173`.

---

## 📡 Sample REST API Endpoints

| Method | Endpoint | Description | Sample Payload / Params |
|---|---|---|---|
| `GET` | `/api/health` | Service health status & DB record counts | None |
| `POST` | `/api/resume/upload` | Ingest PDF/DOCX file, parse, score & persist | `multipart/form-data` with `file` |
| `POST` | `/api/resume/demo` | Load predefined Alex Sharma demo profile | `{}` |
| `POST` | `/api/resume/analyze` | Direct analysis of raw resume text string | `{"text": "Alex Sharma... Python, Flask"}` |
| `GET` | `/api/jobs` | Retrieve all dataset jobs with query filters | `?search=python&job_type=full-time` |
| `GET` | `/api/jobs/<id>` | Retrieve single job specifications | None |
| `POST` | `/api/job/match` | Match resume text against target job description | `{"title": "Backend Dev", "description": "...", "resume_text": "..."}` |
| `POST` | `/api/recommendations` | Rank dataset jobs against resume | `{"resume_text": "...", "top_n": 10}` |
| `GET` | `/api/history` | Retrieve previous analysis records | None |
| `DELETE` | `/api/history/<id>` | Delete single history entry | None |

---

## 🎯 Testing The Application (Demo Walkthrough)

1. Open `http://localhost:5173/` in your browser.
2. Click **"Try Demo Profile (Alex Sharma)"** on the landing page or navbar to load a rich pre-built candidate profile.
3. Observe the **Dashboard**:
   - Circular score gauge (e.g. 85/100).
   - Extracted candidate credentials (B.Tech Computer Science, Apex Institute).
   - Skill category breakdown bar chart.
   - Top 3 recommended job roles with matching/missing skills.
4. Open **"Resume Analysis"** from the sidebar to inspect:
   - Categorized skills (Python, SQL, Flask, Pandas, Git, ML).
   - ATS compatibility breakdown with individual sub-scores.
   - Strengths, Identified Gaps, and Actionable Recommendations.
5. Open **"Job Matching"**:
   - Select a job from the preset dropdown (e.g., *Senior Backend Engineer*) or paste a custom job description.
   - Click **"Analyze Resume Match"** to view real-time TF-IDF Cosine Similarity and skill gap comparison.
6. Open **"Job Recommendations"**:
   - Filter jobs by type (*Remote*, *Full-time*) or location (*Bengaluru*, *Pune*).
   - Click **"View Match Breakdown"** to view the Job Details page with an interactive Skill Gap Pie Chart.
7. Open **"Resume Improvement"** to interact with the ATS checklist and section audits.
8. Open **"Analysis History"** to verify that sessions are persisted in SQLite.
9. Toggle **Dark / Light Mode** via the theme button on the top right.

---

## 🎓 Academic Viva Highlights

- **Text Preprocessing:** Case folding, tech token preservation (`C++`, `.NET`), punctuation filtering, and stopword removal.
- **TF-IDF Weighting:** Computes the statistical significance of keywords within document collections.
- **Cosine Metric:** Normalizes for document length by evaluating the angle $\theta$ between feature vectors.
- **Zero Paid API Dependencies:** Fully deterministic, offline Python ML stack suitable for college presentations.

---

## 📜 License & Academic Disclaimer

This project was developed for academic, educational, and laboratory demonstration purposes. The AI scoring and recommendation metrics are designed as screening aids and do not constitute legal hiring decisions.
