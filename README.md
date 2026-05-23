# 🔮 HireLens AI

**Premium AI-Powered Resume Analyzer** — A production-grade recruitment intelligence platform built with Python, Streamlit, and scikit-learn.

> LinkedIn × ChatGPT × Apple Design — Dark glassmorphism UI with real ML models.

---

## ✨ Features

| Feature | Technology |
|---|---|
| Resume text extraction | pdfplumber |
| NLP preprocessing | NLTK (tokenize → stopwords → lemmatize) |
| Role classification | Multinomial Naive Bayes + TF-IDF |
| ATS scoring | TF-IDF cosine similarity |
| Hire probability | Logistic Regression (L2, lbfgs) |
| Candidate persona | K-Means Clustering (k=4) |
| Cluster visualization | Hierarchical Clustering (Ward linkage) |
| Dimensionality reduction | PCA (2 components) |
| Skill extraction | Custom NLP lexicon |
| AI suggestions | Rule-based + optional Claude API |
| PDF report | fpdf2 branded report |
| Premium UI | Glassmorphism dark theme |

---

## 🧠 ML Concepts Covered

- **Naive Bayes** — Multinomial NB for multi-class text classification across 8 job roles
- **Logistic Regression** — Hire probability prediction with L2 regularization
- **Text Classification** — TF-IDF feature extraction with (1,2)-gram support
- **K-Means Clustering** — Candidate persona detection from feature vectors
- **Hierarchical Clustering** — Ward linkage dendrogram for batch candidate analysis
- **PCA** — 2D principal component visualization of the candidate feature space
- **Evaluation Metrics** — Accuracy, F1 (macro/weighted), AUC-ROC
- **NLP Preprocessing** — Tokenization, stopword removal, lemmatization, TF-IDF

---

## 📁 Project Structure

```
hirelens_ai/
├── app.py                    # Main entry point + navigation
├── requirements.txt
├── README.md
│
├── pages/
│   ├── __init__.py
│   ├── home.py               # Landing page
│   ├── upload.py             # Resume upload + extraction
│   ├── analysis.py           # Core ML analysis dashboard
│   ├── recruiter.py          # Recruiter batch dashboard
│   ├── candidate.py          # Candidate personal view
│   └── report.py             # PDF report generation
│
├── utils/
│   ├── __init__.py
│   ├── styles.py             # Global CSS (glassmorphism, animations)
│   ├── session.py            # Streamlit session state management
│   ├── nlp_utils.py          # NLP pipeline + skill extraction + ATS
│   ├── pdf_utils.py          # PDF/TXT text extraction
│   └── charts.py             # Plotly dark-theme chart helpers
│
├── models/
│   ├── __init__.py
│   ├── ml_models.py          # All ML models (NB, LR, KMeans, PCA)
│   ├── suggestions.py        # AI improvement suggestions engine
│   └── report_gen.py         # fpdf2 PDF report generator
│
└── data/
    ├── sample_resume.txt     # Sample resume for testing
    └── sample_jd.txt         # Sample job description
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hirelens-ai.git
cd hirelens-ai
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# or
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK data

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Testing with Sample Data

1. Navigate to **Upload Resume** page
2. Upload `data/sample_resume.txt`
3. Paste contents of `data/sample_jd.txt` into the Job Description field
4. Enter a candidate name (e.g. "Alex Chen")
5. Click **Run Full Analysis**

---

## ☁️ Deployment

### Streamlit Community Cloud (Free)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set `app.py` as entry point
4. Deploy!

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t hirelens-ai .
docker run -p 8501:8501 hirelens-ai
```

### Render / Railway / Fly.io

Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

---

## 🔑 Optional: Claude AI Integration

To enable AI-powered resume suggestions via Claude API:

1. Get an API key at [console.anthropic.com](https://console.anthropic.com)
2. Add to Streamlit secrets (`~/.streamlit/secrets.toml`):

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

3. The suggestions engine will automatically use Claude for personalized tips.

---

## 📊 ML Model Details

### Naive Bayes Classifier
- **Model**: `sklearn.naive_bayes.MultinomialNB(alpha=0.5)`
- **Features**: TF-IDF with (1,2)-gram, max 5000 features, sublinear_tf=True
- **Classes**: 8 job roles (Data Scientist, ML Engineer, Data Analyst, etc.)
- **Training data**: 40 curated resume snippets (5 per role)

### Logistic Regression
- **Model**: `sklearn.linear_model.LogisticRegression(C=1.0, solver='lbfgs')`
- **Features**: [ATS score, skill count, word count, role ID]
- **Regularization**: L2
- **Training**: 200 synthetic samples with realistic hiring signal noise

### K-Means Clustering
- **Model**: `sklearn.cluster.KMeans(n_clusters=4, init='k-means++')`
- **Features**: Standardized [ATS, skills, words, hire probability]
- **Personas**: Rising Star, Top Performer, Growth Potential, Technical Specialist

### PCA
- **Model**: `sklearn.decomposition.PCA(n_components=2)`
- **Input**: 5-dimensional standardized feature space
- **Output**: 2D visualization for cluster scatter plot

### Hierarchical Clustering
- **Library**: `scipy.cluster.hierarchy`
- **Linkage**: Ward
- **Distance**: Euclidean
- **Visualization**: Plotly dendrogram

---

## 🎨 UI Design System

| Token | Value |
|---|---|
| Background | `#0F1117` |
| Secondary BG | `#161B27` |
| Accent | `#7C3AED` |
| Text Primary | `#F0F0F5` |
| Text Secondary | `#9CA3AF` |
| Display Font | Syne (800 weight) |
| Body Font | DM Sans |
| Mono Font | JetBrains Mono |
| Border Radius | 8px / 14px / 20px / 28px |

---

## 📄 License

MIT License — Free for academic and commercial use.

---

## 🙏 Built With

- [Streamlit](https://streamlit.io) — App framework
- [scikit-learn](https://scikit-learn.org) — ML models
- [NLTK](https://nltk.org) — NLP preprocessing
- [Plotly](https://plotly.com) — Interactive charts
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF extraction
- [fpdf2](https://py-pdf.github.io/fpdf2/) — PDF generation
- [SciPy](https://scipy.org) — Hierarchical clustering
