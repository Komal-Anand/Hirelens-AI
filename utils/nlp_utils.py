"""
utils/nlp_utils.py — NLP preprocessing pipeline.
Gracefully degrades when NLTK is unavailable.
"""

import re
import string
from collections import Counter

# ── Try NLTK; fall back to simple tokenizer ───────────────────────────────────
try:
    import nltk
    for pkg in ["punkt", "stopwords", "wordnet", "punkt_tab"]:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass
    from nltk.corpus import stopwords as nltk_stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize as nltk_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

ENGLISH_STOPWORDS = {
    "i","me","my","myself","we","our","ours","ourselves","you","your","yours",
    "he","him","his","she","her","hers","it","its","they","them","their","theirs",
    "what","which","who","whom","this","that","these","those","am","is","are","was",
    "were","be","been","being","have","has","had","do","does","did","will","would",
    "shall","should","may","might","must","can","could","a","an","the","and","but",
    "or","nor","for","so","yet","at","by","in","of","on","to","up","as","if","no",
    "not","with","from","into","about","than","then","when","where","how","all",
    "also","more","such","other","than","just","over","only","both","each",
}

TECH_SKILLS = {
    "python", "java", "javascript", "typescript", "c++", "c#", "r", "scala",
    "sql", "nosql", "mongodb", "postgresql", "mysql", "sqlite", "redis",
    "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
    "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "neural networks", "transformers", "bert", "gpt",
    "aws", "gcp", "azure", "docker", "kubernetes", "ci/cd", "git", "github",
    "react", "angular", "vue", "node.js", "fastapi", "flask", "django",
    "spark", "hadoop", "kafka", "airflow", "dbt", "snowflake", "bigquery",
    "tableau", "power bi", "looker", "excel", "powerpoint",
    "agile", "scrum", "jira", "confluence", "linux", "bash", "shell",
    "rest api", "graphql", "microservices", "data engineering",
    "feature engineering", "model deployment", "mlops", "devops",
    "statistics", "probability", "calculus", "linear algebra",
    "data analysis", "data visualization", "data science", "analytics",
    "a/b testing", "hypothesis testing", "regression", "classification",
    "clustering", "time series", "forecasting", "recommendation systems",
}

SOFT_SKILLS = {
    "leadership", "communication", "teamwork", "problem solving",
    "critical thinking", "project management", "mentoring", "collaboration",
    "creativity", "adaptability", "presentation", "stakeholder management",
}

ALL_SKILLS = TECH_SKILLS | SOFT_SKILLS

ROLE_REQUIRED_SKILLS = {
    "Data Scientist":    ["python", "machine learning", "statistics", "sql", "pandas", "scikit-learn"],
    "ML Engineer":       ["python", "tensorflow", "pytorch", "docker", "mlops", "model deployment"],
    "Data Analyst":      ["sql", "excel", "tableau", "data analysis", "statistics", "python"],
    "Backend Engineer":  ["python", "java", "sql", "rest api", "docker", "git"],
    "Frontend Engineer": ["javascript", "react", "css", "typescript", "git"],
    "Data Engineer":     ["python", "spark", "sql", "airflow", "kafka", "aws"],
    "DevOps Engineer":   ["docker", "kubernetes", "ci/cd", "aws", "linux", "bash"],
    "Full Stack":        ["javascript", "react", "node.js", "sql", "git", "rest api"],
}


def _simple_tokenize(text: str) -> list:
    text = text.lower()
    tokens = re.findall(r'\b[a-z][a-z0-9\+\#\.]*\b', text)
    return tokens


def _simple_lemmatize(word: str) -> str:
    suffixes = [("ing", ""), ("tion", "te"), ("tions", "te"),
                ("ment", ""), ("ments", ""), ("ers", "er"),
                ("ies", "y"), ("es", ""), ("s", "")]
    for suf, rep in suffixes:
        if word.endswith(suf) and len(word) - len(suf) > 3:
            return word[:-len(suf)] + rep
    return word


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\+?\d[\d\s\-().]{7,}\d", " ", text)
    text = re.sub(r"[^\w\s\+#/]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_and_lemmatize(text: str) -> list:
    cleaned = clean_text(text)
    if NLTK_AVAILABLE:
        try:
            from nltk.tokenize import word_tokenize
            from nltk.corpus import stopwords
            from nltk.stem import WordNetLemmatizer
            tokens = word_tokenize(cleaned)
            stop = set(stopwords.words("english"))
            tokens = [t for t in tokens if t not in stop and len(t) > 2]
            lem = WordNetLemmatizer()
            return [lem.lemmatize(t) for t in tokens]
        except Exception:
            pass
    # Fallback
    tokens = _simple_tokenize(cleaned)
    tokens = [t for t in tokens if t not in ENGLISH_STOPWORDS and len(t) > 2]
    return [_simple_lemmatize(t) for t in tokens]


def extract_skills(text: str) -> list:
    text_lower = text.lower()
    found = []
    for skill in ALL_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found.append(skill)
    return sorted(set(found))


def compute_missing_skills(found_skills: list, role: str) -> list:
    required = ROLE_REQUIRED_SKILLS.get(role, [])
    found_lower = {s.lower() for s in found_skills}
    return [s for s in required if s.lower() not in found_lower]


def get_top_keywords(text: str, n: int = 20) -> list:
    tokens = tokenize_and_lemmatize(text)
    tokens = [t for t in tokens if len(t) > 3]
    freq = Counter(tokens)
    return freq.most_common(n)


def compute_tfidf_ats(resume_text: str, job_description: str) -> float:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    if not job_description or not resume_text:
        tokens = tokenize_and_lemmatize(resume_text)
        unique_ratio = len(set(tokens)) / max(len(tokens), 1)
        skill_count = len(extract_skills(resume_text))
        score = min(100, int(unique_ratio * 60 + skill_count * 3))
        return max(20, score)

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        tfidf = vectorizer.fit_transform([resume_text, job_description])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return round(float(sim) * 100, 1)
    except Exception:
        return 50.0
