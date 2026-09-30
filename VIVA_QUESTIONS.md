# 🎓 COLLEGE VIVA VOCE QUESTIONS & ANSWERS
## AI Resume Screening & Job Recommendation System

Comprehensive viva examination preparation covering Natural Language Processing (NLP), Machine Learning, TF-IDF Vectorization, Similarity Metrics, System Architecture, and Software Engineering.

---

### 1. What is Natural Language Processing (NLP)?
**Answer:**  
Natural Language Processing (NLP) is a branch of Artificial Intelligence that enables computers to understand, interpret, and manipulate human language. In this project, NLP techniques are used to clean resume text, remove stopwords, extract entities (skills, degrees, experiences), and convert unstructured text into mathematical vectors for similarity computation.

---

### 2. What is TF-IDF and how does it work?
**Answer:**  
TF-IDF stands for **Term Frequency - Inverse Document Frequency**. It is a statistical numerical statistic that reflects how important a word is to a document in a collection or corpus.
- **Term Frequency (TF):** Measures how frequently a term occurs in a document.
  $$\text{TF}(t, d) = \frac{\text{Count of term } t \text{ in document } d}{\text{Total words in } d}$$
- **Inverse Document Frequency (IDF):** Measures how rare or common a word is across all documents.
  $$\text{IDF}(t, D) = \log\left(\frac{|D|}{1 + |\{d \in D : t \in d\}|}\right)$$
- **TF-IDF:** $\text{TF-IDF} = \text{TF} \times \text{IDF}$. Common words like "the" receive low weights, while domain keywords like "PyTorch" or "PostgreSQL" receive high weights.

---

### 3. Why is TF-IDF preferred over simple Word Count or Bag-of-Words (BoW)?
**Answer:**  
Simple word count / Bag-of-Words merely tallies word occurrences. Ubiquitous words (e.g., "system", "experience", "developed") would dominate the count and skew similarity. TF-IDF down-weights ubiquitous terms and amplifies specialized keywords that uniquely define a candidate’s expertise.

---

### 4. What is Cosine Similarity and what is its formula?
**Answer:**  
Cosine Similarity measures the cosine of the angle between two non-zero vectors in multi-dimensional space.
$$\text{Cosine Similarity}(\mathbf{A}, \mathbf{B}) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\|_2 \|\mathbf{B}\|_2} = \frac{\sum_{i=1}^n A_i B_i}{\sqrt{\sum_{i=1}^n A_i^2} \sqrt{\sum_{i=1}^n B_i^2}}$$
The resulting value ranges from `0.0` (completely orthogonal/unrelated) to `1.0` (identical orientation).

---

### 5. Why is Cosine Similarity chosen over Euclidean Distance for text matching?
**Answer:**  
Euclidean distance measures the straight-line distance between vector endpoints, which is heavily influenced by document length (a 2-page detailed resume will have large vector magnitudes and thus a large distance from a concise job description). Cosine similarity measures the directional angle $\theta$, effectively normalizing for document length.

---

### 6. What is a Recommendation System and how is it implemented in this project?
**Answer:**  
A recommendation system suggests relevant items to users based on preference patterns. In this project, a **Content-Based Filtering** recommendation engine is implemented:
1. The candidate resume is converted into a TF-IDF vector.
2. All 52 job descriptions in `jobs.csv` are vectorized into the same vector space.
3. Pairwise Cosine Similarity and Jaccard Skill Overlap are calculated.
4. Jobs are sorted and ranked by composite match score descending.

---

### 7. What is the Jaccard Similarity Index?
**Answer:**  
Jaccard similarity measures the overlap between two finite sample sets.
$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
In this project, it is used to evaluate the exact intersection ratio between candidate skills and job requirements.

---

### 8. What is the Hybrid Recommendation Formula used in this project?
**Answer:**  
$$\text{Match Score} = (0.55 \times \text{TF-IDF Cosine Similarity}) + (0.45 \times \text{Skill Overlap Ratio})$$
This combines contextual semantic understanding (55%) with strict requirement satisfaction (45%).

---

### 9. How does Resume Parsing work without paid AI APIs?
**Answer:**  
1. **Document Reading:** `pdfplumber`, `PyPDF2`, or `python-docx` extract raw text streams.
2. **Text Normalization:** Lowercasing, punctuation stripping (while preserving `C++`, `C#`, `.NET`), and stopword removal.
3. **Regex & Entity Heuristics:**
   - Emails via RFC 5322 regex.
   - Phone numbers via international digit patterns.
   - Degrees via pattern matching (`B.Tech`, `B.Sc`, `M.Tech`, `BCA`).
   - Skills via regex token boundary matching against `skills_taxonomy.json`.

---

### 10. How is the Overall Academic Resume Score calculated?
**Answer:**  
The overall screening score is a weighted sum across 6 academic dimensions:
- **Skills Match & Diversity:** 35%
- **Work Experience Depth:** 20%
- **Project Portfolio Quality:** 15%
- **Educational Qualification:** 10%
- **Resume Completeness:** 10%
- **Keyword Relevance & Action Verbs:** 10%

$$\text{Overall Score} = \sum (\text{Dimension Score}_i \times \text{Weight}_i)$$

---

### 11. What is an Applicant Tracking System (ATS)?
**Answer:**  
An ATS is software utilized by employers to collect, sort, scan, and rank job applications. In this project, the ATS simulator audits:
1. **Keyword Optimization:** Density of technical terminology and action verbs.
2. **Structural Integrity:** Standard section headings and readable contact headers.
3. **Skills Coverage:** Technical depth across programming languages, databases, and DevOps.

---

### 12. What is Text Preprocessing and why is it essential in NLP?
**Answer:**  
Text preprocessing converts noisy, raw textual data into clean, normalized tokens. Steps include:
- **Case Folding:** Converting all characters to lowercase so "Python" and "python" match.
- **Punctuation Removal:** Stripping commas, colons, and hyphens.
- **Stopword Removal:** Eliminating non-discriminative words like "and", "the", "with".
- **Tokenization:** Splitting sentences into discrete word tokens.

---

### 13. How are multi-word technical skills (e.g., "Machine Learning", "Spring Boot") handled?
**Answer:**  
1. In TF-IDF vectorization, an n-gram range of `(1, 2)` is used, generating both unigrams ("machine", "learning") and bigrams ("machine learning").
2. In the skill extractor, candidate patterns are sorted by length descending and matched using phrase boundary regexes.

---

### 14. What are N-grams?
**Answer:**  
An n-gram is a contiguous sequence of $n$ items from a given text.
- Unigram ($n=1$): "Python", "Developer"
- Bigram ($n=2$): "Machine Learning", "REST API"
- Trigram ($n=3$): "Natural Language Processing"

---

### 15. Why use Flask for the backend?
**Answer:**  
Flask is a lightweight, flexible Python WSGI web framework. It has minimal overhead, supports modular blueprints, integrates seamlessly with Python data science libraries (Scikit-learn, NumPy, Pandas), and allows building clean RESTful JSON endpoints.

---

### 16. Why use React with Vite for the frontend?
**Answer:**  
- **React:** Component-driven architecture allows reusable UI widgets (ScoreGauge, SkillBadge, Charts).
- **Vite:** Next-generation frontend build tool providing lightning-fast Hot Module Replacement (HMR) and optimized Rollup bundling.

---

### 17. Why use SQLite and SQLAlchemy?
**Answer:**  
- **SQLite:** Serverless, zero-configuration relational database stored as a single file (`resume_system.db`), making the project portable and easy to run on any computer.
- **SQLAlchemy:** Python ORM that abstracts SQL queries into Python classes (`Resume`, `ResumeAnalysis`, `Job`, `AnalysisHistory`).

---

### 18. What is CORS and why is `flask-cors` needed?
**Answer:**  
CORS stands for **Cross-Origin Resource Sharing**. Because the frontend runs on port `5173` and the Flask backend runs on port `5000`, the browser's Same-Origin Policy blocks API calls by default. `flask-cors` configures HTTP response headers (`Access-Control-Allow-Origin: *`) to allow secure cross-origin communication.

---

### 19. How does the system avoid hallucinating resume information?
**Answer:**  
Unlike generative LLMs that may hallucinate non-existent details, this project uses deterministic extraction: if a phone number, degree, or skill is not explicitly detected via regex and dictionary parsing, the system explicitly marks it as `"Not detected"`.

---

### 20. How does the system protect tech skills like `C++`, `C#`, and `.NET` during punctuation stripping?
**Answer:**  
Before punctuation removal, regex preprocessors substitute special symbols with unique placeholders (e.g., `C++` $\rightarrow$ `cpp_tech`, `C#` $\rightarrow$ `csharp_tech`, `.NET` $\rightarrow$ `dotnet_tech`). After stripping other punctuation, the placeholders are restored to their canonical names.

---

### 21. What is the difference between Supervised and Unsupervised Learning?
**Answer:**  
- **Supervised Learning:** Models are trained on labeled input-output pairs (e.g., classifying emails as spam/ham).
- **Unsupervised Learning:** Algorithms find underlying patterns in unlabeled data (e.g., K-Means clustering).
- **In this project:** We employ deterministic NLP vector space modeling and cosine distance metrics without requiring massive labeled training sets.

---

### 22. What are Action Verbs and why are they evaluated in resumes?
**Answer:**  
Action verbs (e.g., *engineered, built, optimized, deployed, architected*) convey leadership and technical execution. Resumes with strong action verbs achieve higher keyword relevance and ATS structure scores.

---

### 23. What dataset does the system use for job recommendations?
**Answer:**  
The system uses `backend/data/jobs.csv`, a dataset of **52 curated technology job postings** across roles like Python Developer, Data Scientist, ML Engineer, React Developer, DevOps, and Java Architect.

---

### 24. What is the purpose of the Analysis History table?
**Answer:**  
The `analysis_history` table in SQLite logs past candidate screenings with timestamps, overall scores, ATS ratings, and top matched job titles. Users can reload any past session with one click.

---

### 25. What is sublinear TF scaling in Scikit-learn's TfidfVectorizer?
**Answer:**  
Sublinear TF replaces raw term frequency $\text{TF}$ with $1 + \log(\text{TF})$. This dampens the influence of a word appearing 20 times versus 2 times (a term occurring 20 times is not 10 times more important than a term occurring twice).

---

### 26. What happens if an uploaded PDF is password-protected or corrupt?
**Answer:**  
The backend catches `PdfReadError` or file exceptions, aborts gracefully, and returns a clean JSON error response (`status: 400`) notifying the user to upload an unencrypted, valid document.

---

### 27. What are the limitations of this project?
**Answer:**  
1. Scanned image-only PDFs without text layers require an OCR engine like Tesseract.
2. Extremely non-standard multi-column graphical resumes may disrupt section sequence.
3. Job recommendations are bound to the internal dataset collection (easily expandable via CSV/DB).

---

### 28. How can this project be extended in the future?
**Answer:**  
- Adding Tesseract OCR for scanned physical documents.
- Integrating lightweight local Transformer sentence embeddings (e.g., MiniLM).
- Recruiter ZIP batch upload portal for bulk candidate ranking.
- Automated resume re-builder that exports an optimized PDF.

---

### 29. Can this project run on any operating system?
**Answer:**  
Yes. Python 3 and Node.js are cross-platform. The application runs identically on Windows 10/11, macOS, and Linux.

---

### 30. How would you summarize the core contribution of this project in 2 sentences?
**Answer:**  
This project delivers a 100% local, transparent AI recruitment platform that parses candidate resumes into structured entities and evaluates ATS compatibility. Using TF-IDF vectorization and Cosine Similarity, it calculates mathematically sound job match scores and skill gaps to assist both recruiters and job seekers.
