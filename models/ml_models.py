"""
models/ml_models.py — All ML models used in HireLens AI.
Covers:
  - Multinomial Naive Bayes (role classification)
  - Logistic Regression (hire probability)
  - K-Means Clustering (candidate persona)
  - Hierarchical Clustering (dendrogram)
  - PCA (dimensionality reduction / visualization)
  - Evaluation Metrics (accuracy, confusion matrix, etc.)
"""

import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ── Scikit-learn imports ──────────────────────────────────────────────────────
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.metrics import (
    accuracy_score, f1_score, classification_report,
    confusion_matrix, roc_auc_score
)

# ── Sample training data ──────────────────────────────────────────────────────
# Each entry: (resume_snippet, role_label)
TRAIN_DATA = [
    # Data Scientist
    ("python machine learning deep learning nlp tensorflow pytorch statistics scikit-learn pandas data modeling", "Data Scientist"),
    ("data science python r statistical modeling hypothesis testing regression classification ensemble methods", "Data Scientist"),
    ("python ml models gradient boosting xgboost cross validation feature engineering sklearn neural network", "Data Scientist"),
    ("machine learning algorithms random forest svm neural network data preprocessing python jupyter notebook", "Data Scientist"),
    ("nlp text classification sentiment analysis bert transformers python pandas scipy matplotlib", "Data Scientist"),

    # ML Engineer
    ("mlops model deployment docker kubernetes fastapi rest api tensorflow serving model optimization", "ML Engineer"),
    ("production ml system model monitoring ci cd pipeline airflow docker kubernetes aws sagemaker", "ML Engineer"),
    ("deep learning model training gpu optimization pytorch distributed training model compression", "ML Engineer"),
    ("ml pipeline feature store model registry mlflow kubeflow vertex ai model serving", "ML Engineer"),
    ("machine learning engineering python tensorflow docker model deployment api integration", "ML Engineer"),

    # Data Analyst
    ("sql tableau power bi excel data visualization business intelligence reporting dashboard kpi", "Data Analyst"),
    ("data analysis excel pivot tables vlookup sql queries reporting stakeholder presentation", "Data Analyst"),
    ("business analytics sql python data visualization tableau dashboard reporting analysis", "Data Analyst"),
    ("data analyst sql queries excel advanced formulas powerpoint presentation business insights", "Data Analyst"),
    ("analytics google analytics mixpanel looker sql a/b testing funnel analysis cohort", "Data Analyst"),

    # Backend Engineer
    ("python java spring boot microservices rest api postgresql redis docker kubernetes git", "Backend Engineer"),
    ("backend development nodejs express mongodb postgresql api design system design scalability", "Backend Engineer"),
    ("java spring framework hibernate mysql redis aws ec2 rds ci cd jenkins microservices", "Backend Engineer"),
    ("python django rest framework postgresql celery redis docker aws lambda serverless", "Backend Engineer"),
    ("golang python grpc postgresql kafka docker kubernetes api gateway microservices", "Backend Engineer"),

    # Frontend Engineer
    ("react javascript typescript html css redux graphql webpack jest testing cypress", "Frontend Engineer"),
    ("frontend development vue angular javascript typescript ui ux design figma responsive", "Frontend Engineer"),
    ("react hooks typescript tailwind css storybook jest testing accessibility performance", "Frontend Engineer"),
    ("javascript es6 react redux webpack babel npm yarn git web performance optimization", "Frontend Engineer"),
    ("nextjs react typescript vercel css modules framer motion animation performance seo", "Frontend Engineer"),

    # Data Engineer
    ("data pipeline spark hadoop kafka airflow etl postgresql snowflake dbt data warehouse", "Data Engineer"),
    ("apache spark python sql data lake aws glue s3 athena redshift kinesis streaming", "Data Engineer"),
    ("data engineering python pyspark kafka confluent bigquery dataflow beam pipeline orchestration", "Data Engineer"),
    ("etl pipelines sql python airflow dbt snowflake looker data modeling warehouse", "Data Engineer"),
    ("databricks spark python delta lake unity catalog data lakehouse azure synapse pipeline", "Data Engineer"),

    # DevOps Engineer
    ("devops kubernetes docker terraform ansible jenkins ci cd aws azure monitoring prometheus grafana", "DevOps Engineer"),
    ("site reliability engineering sre kubernetes helm prometheus alertmanager on call incident", "DevOps Engineer"),
    ("platform engineering kubernetes terraform github actions argocd flux gitops cloud native", "DevOps Engineer"),
    ("devops jenkins docker kubernetes aws cloudformation ansible python bash linux automation", "DevOps Engineer"),
    ("cloud infrastructure aws terraform kubernetes helm monitoring logging elk stack security", "DevOps Engineer"),

    # Full Stack
    ("full stack react nodejs postgresql mongodb rest api docker git agile scrum javascript", "Full Stack"),
    ("fullstack developer react vue python django postgresql docker aws ci cd javascript", "Full Stack"),
    ("react typescript nodejs express mongodb postgresql graphql docker kubernetes deployment", "Full Stack"),
    ("full stack javascript react next.js node express mysql redis docker aws git heroku", "Full Stack"),
    ("mern stack mongodb express react node.js jwt authentication docker deployment git", "Full Stack"),
]


def build_naive_bayes_classifier():
    """
    Train a Multinomial Naive Bayes classifier on resume snippets.
    Returns (vectorizer, model, label_encoder).
    """
    texts  = [d[0] for d in TRAIN_DATA]
    labels = [d[1] for d in TRAIN_DATA]

    le = LabelEncoder()
    y = le.fit_transform(labels)

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True,
        min_df=1,
    )
    X = vectorizer.fit_transform(texts)

    model = MultinomialNB(alpha=0.5)
    model.fit(X, y)

    return vectorizer, model, le


def classify_resume(resume_text: str):
    """
    Predict the most likely job role using Naive Bayes.
    Returns:
        predicted_role (str),
        role_probabilities (dict: role → probability),
        eval_metrics (dict)
    """
    vectorizer, model, le = build_naive_bayes_classifier()

    X_input = vectorizer.transform([resume_text])
    probs = model.predict_proba(X_input)[0]
    classes = le.classes_

    role_probs = {cls: float(p) for cls, p in zip(classes, probs)}
    predicted_idx = np.argmax(probs)
    predicted_role = classes[predicted_idx]

    # Leave-one-out style eval metrics (on training data)
    texts  = [d[0] for d in TRAIN_DATA]
    labels = [d[1] for d in TRAIN_DATA]
    y_true = le.transform(labels)
    X_train = vectorizer.transform(texts)
    y_pred = model.predict(X_train)

    eval_metrics = {
        "accuracy": round(accuracy_score(y_true, y_pred) * 100, 1),
        "f1_macro": round(f1_score(y_true, y_pred, average="macro") * 100, 1),
        "model": "Multinomial Naive Bayes",
        "features": "TF-IDF (1,2)-grams",
        "classes": len(classes),
    }

    return predicted_role, role_probs, eval_metrics


def predict_hire_probability(
    resume_text: str,
    ats_score: float,
    skill_count: int,
    word_count: int,
    role: str,
) -> tuple[float, dict]:
    """
    Logistic Regression to estimate hiring probability.
    Features: ats_score, skill_count, word_count, role_encoded.
    Returns (probability_float, feature_importance_dict).
    """
    # Synthetic training data mimicking real hiring signals
    np.random.seed(42)
    n_samples = 200

    # Features: [ats, skills, words, role_id]
    ats_vals   = np.random.uniform(10, 100, n_samples)
    skill_vals = np.random.randint(2, 25, n_samples)
    word_vals  = np.random.randint(100, 1500, n_samples)
    role_vals  = np.random.randint(0, 8, n_samples)

    # Hire label: ATS > 60, skills > 8, words 300-900 → more likely hired
    y_train = ((ats_vals > 55) & (skill_vals > 6) & (word_vals > 250)).astype(int)
    # Add noise
    flip_idx = np.random.choice(n_samples, size=20, replace=False)
    y_train[flip_idx] = 1 - y_train[flip_idx]

    X_train = np.column_stack([ats_vals, skill_vals, word_vals, role_vals])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)

    lr = LogisticRegression(max_iter=300, C=1.0, solver="lbfgs")
    lr.fit(X_scaled, y_train)

    # Encode current role
    roles = ["Data Scientist", "ML Engineer", "Data Analyst", "Backend Engineer",
             "Frontend Engineer", "Data Engineer", "DevOps Engineer", "Full Stack"]
    role_id = roles.index(role) if role in roles else 0

    X_input = np.array([[ats_score, skill_count, word_count, role_id]])
    X_input_scaled = scaler.transform(X_input)

    prob = float(lr.predict_proba(X_input_scaled)[0][1])

    # Feature importance (coefficients)
    coefs = lr.coef_[0]
    feature_names = ["ATS Score", "Skill Count", "Word Count", "Role Match"]
    importance = {n: round(float(abs(c)) * 100, 1) for n, c in zip(feature_names, coefs)}

    eval_metrics = {
        "model": "Logistic Regression",
        "solver": "lbfgs",
        "regularization": "L2 (C=1.0)",
        "train_accuracy": round(accuracy_score(y_train, lr.predict(X_scaled)) * 100, 1),
    }

    return round(prob, 4), importance, eval_metrics


def cluster_candidates(resume_features: list[dict], n_clusters: int = 4):
    """
    K-Means clustering on candidate feature vectors.
    Features: [ats_score, skill_count, word_count, hire_prob]
    Returns (cluster_labels, cluster_personas, kmeans_model, scaler).
    """
    # Persona labels per cluster index
    PERSONA_NAMES = [
        "🚀 Rising Star",
        "💎 Top Performer",
        "📈 Growth Potential",
        "🔧 Technical Specialist",
    ]

    if len(resume_features) < n_clusters:
        n_clusters = max(2, len(resume_features))

    X = np.array([
        [f.get("ats", 50), f.get("skills", 5), f.get("words", 300), f.get("prob", 0.5)]
        for f in resume_features
    ])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    # Map cluster index → persona (by centroid ATS score rank)
    centroids = kmeans.cluster_centers_
    ats_order = np.argsort(-centroids[:, 0])  # descending ATS
    persona_map = {old: PERSONA_NAMES[new % len(PERSONA_NAMES)]
                   for new, old in enumerate(ats_order)}
    personas = [persona_map[l] for l in labels]

    eval_metrics = {
        "model": "K-Means",
        "k": n_clusters,
        "inertia": round(float(kmeans.inertia_), 2),
        "algorithm": "lloyd",
        "init": "k-means++",
    }

    return labels.tolist(), personas, kmeans, scaler, eval_metrics


def run_pca(features: list[dict], labels: list[str] = None):
    """
    PCA for 2D visualization of candidate feature space.
    Returns a DataFrame-ready dict.
    """
    import pandas as pd

    X = np.array([
        [f.get("ats", 50), f.get("skills", 5), f.get("words", 300),
         f.get("prob", 0.5), f.get("role_id", 0)]
        for f in features
    ])

    if X.shape[0] < 2:
        return None

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    n_components = min(2, X.shape[1], X.shape[0])
    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    result = {
        "PC1": X_pca[:, 0].tolist(),
        "PC2": (X_pca[:, 1].tolist() if n_components > 1 else [0.0] * len(X_pca)),
        "Label": labels or [f"C{i}" for i in range(len(features))],
        "Cluster": [f.get("cluster", 0) for f in features],
        "explained_variance": [round(v * 100, 1) for v in pca.explained_variance_ratio_],
    }
    return result


def compute_evaluation_metrics(y_true, y_pred, y_prob=None):
    """
    General evaluation utility.
    Returns accuracy, F1, and optionally AUC.
    """
    metrics = {
        "accuracy": round(accuracy_score(y_true, y_pred) * 100, 2),
        "f1_weighted": round(f1_score(y_true, y_pred, average="weighted") * 100, 2),
    }
    if y_prob is not None:
        try:
            metrics["auc_roc"] = round(roc_auc_score(y_true, y_prob) * 100, 2)
        except Exception:
            pass
    return metrics
