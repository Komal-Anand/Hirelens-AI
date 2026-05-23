"""
models/suggestions.py — AI-powered resume improvement suggestions.
Rule-based + Claude-API-powered (when API key available) suggestions.
"""

# import streamlit as st  # optional
import requests
import json


SUGGESTION_RULES = [
    {
        "check": lambda data: data.get("word_count", 0) < 300,
        "icon": "📝",
        "title": "Expand Your Resume",
        "text": "Your resume is quite brief. Aim for 400–700 words highlighting achievements, not just duties. Quantify impact where possible (e.g., 'Improved model accuracy by 12%').",
        "priority": 1,
    },
    {
        "check": lambda data: data.get("word_count", 0) > 1200,
        "icon": "✂️",
        "title": "Trim for Clarity",
        "text": "Recruiters spend ~7 seconds on first scan. Keep your resume under 900 words. Remove older than 10-year experience and irrelevant details.",
        "priority": 2,
    },
    {
        "check": lambda data: data.get("skill_count", 0) < 5,
        "icon": "🔧",
        "title": "Add More Technical Skills",
        "text": "You've listed fewer than 5 skills. Add a dedicated 'Skills' section with technologies, frameworks, and tools relevant to your target role.",
        "priority": 1,
    },
    {
        "check": lambda data: data.get("ats_score", 100) < 50,
        "icon": "🤖",
        "title": "Improve ATS Compatibility",
        "text": "Your ATS score is below 50%. Mirror keywords from the job description naturally in your resume. Avoid tables, headers, and graphics that ATS parsers struggle with.",
        "priority": 1,
    },
    {
        "check": lambda data: len(data.get("missing_skills", [])) > 3,
        "icon": "📚",
        "title": "Close Critical Skill Gaps",
        "text": f"Several key skills are missing. Consider adding projects or certifications demonstrating these: {', '.join([])}.",
        "priority": 1,
        "dynamic_missing": True,
    },
    {
        "check": lambda data: data.get("hire_prob", 1.0) < 0.45,
        "icon": "📊",
        "title": "Strengthen Quantifiable Achievements",
        "text": "Low hire probability detected. Convert task descriptions to achievement statements. Use metrics: 'Reduced pipeline latency by 35%' beats 'Worked on pipelines'.",
        "priority": 1,
    },
    {
        "check": lambda data: "github" not in data.get("text_lower", ""),
        "icon": "💻",
        "title": "Add Your GitHub Profile",
        "text": "No GitHub link detected. Include a GitHub profile link — it's one of the top signals recruiters look for in technical roles.",
        "priority": 2,
    },
    {
        "check": lambda data: "linkedin" not in data.get("text_lower", ""),
        "icon": "🔗",
        "title": "Add LinkedIn URL",
        "text": "LinkedIn URL not found. Always include your LinkedIn profile for credibility and easier recruiter outreach.",
        "priority": 2,
    },
    {
        "check": lambda data: not any(w in data.get("text_lower", "") for w in ["certif", "award", "honor"]),
        "icon": "🏆",
        "title": "Highlight Certifications",
        "text": "No certifications or awards detected. Add relevant certifications (AWS, GCP, Coursera, etc.) to stand out in competitive candidate pools.",
        "priority": 3,
    },
    {
        "check": lambda data: not any(w in data.get("text_lower", "") for w in ["project", "built", "developed", "created", "designed"]),
        "icon": "🚀",
        "title": "Showcase Projects",
        "text": "No project keywords detected. Add a 'Projects' section with 2-3 relevant projects. Include tech stack, your role, and measurable outcomes.",
        "priority": 2,
    },
    {
        "check": lambda data: not any(w in data.get("text_lower", "") for w in ["%", "percent", "million", "thousand", "increased", "decreased", "improved", "reduced"]),
        "icon": "📈",
        "title": "Quantify Your Impact",
        "text": "No measurable impact found. Add numbers: revenue influenced, users served, performance improvements. Data-driven resumes get 40% more callbacks.",
        "priority": 1,
    },
    {
        "check": lambda data: data.get("role") in ["Data Scientist", "ML Engineer"] and "publication" not in data.get("text_lower", "") and "research" not in data.get("text_lower", ""),
        "icon": "🔬",
        "title": "Add Research or Publications",
        "text": "For Data Science / ML roles, referencing research experience or publications (even blog posts / Kaggle) significantly boosts perceived expertise.",
        "priority": 3,
    },
]


def generate_suggestions(
    resume_text: str,
    ats_score: float,
    hire_prob: float,
    role: str,
    missing_skills: list,
    word_count: int,
    skill_count: int,
) -> list[dict]:
    """
    Generate ranked improvement suggestions.
    Returns list of {icon, title, text, priority} dicts sorted by priority.
    """
    text_lower = resume_text.lower()
    data = {
        "text_lower": text_lower,
        "ats_score": ats_score,
        "hire_prob": hire_prob,
        "role": role,
        "missing_skills": missing_skills,
        "word_count": word_count,
        "skill_count": skill_count,
    }

    results = []
    for rule in SUGGESTION_RULES:
        try:
            if rule["check"](data):
                suggestion = {
                    "icon": rule["icon"],
                    "title": rule["title"],
                    "text": rule["text"],
                    "priority": rule["priority"],
                }
                # Dynamic missing skills injection
                if rule.get("dynamic_missing") and missing_skills:
                    suggestion["text"] = (
                        f"Several key skills are missing for a {role} role. "
                        f"Consider demonstrating: {', '.join(missing_skills[:5])}. "
                        f"Add relevant projects, courses, or certifications."
                    )
                results.append(suggestion)
        except Exception:
            pass

    # Sort by priority (1 = high, 3 = low)
    results.sort(key=lambda x: x["priority"])
    return results[:8]  # Max 8 suggestions


def get_ai_powered_suggestion(resume_text: str, role: str) -> str | None:
    """
    Optional: Call Claude API for a personalized suggestion paragraph.
    Returns None if API not configured or fails.
    """
    try:
        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 300,
            "messages": [{
                "role": "user",
                "content": (
                    f"You are a senior technical recruiter. Given this resume excerpt for a "
                    f"'{role}' position, provide ONE specific, actionable improvement tip in 2-3 sentences. "
                    f"Be direct and specific. No fluff. Resume excerpt:\n\n{resume_text[:800]}"
                )
            }]
        }
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data["content"][0]["text"]
    except Exception:
        pass
    return None
