"""
models/report_gen.py — PDF report generation using fpdf2.
Generates a branded HireLens AI analysis report.
"""

from datetime import datetime
import io
import os


def clean_pdf_text(text):
    """Return a PDF-safe string by removing unsupported characters."""
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        "•": "-",
        "·": "-",
        "—": "-",
        "–": "-",
        "’": "'",
        "“": '"',
        "”": '"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "ignore").decode("latin-1")


def generate_pdf_report(
    candidate_name: str,
    role: str,
    ats_score: float,
    hire_prob: float,
    cluster_label: str,
    skills: list,
    missing_skills: list,
    suggestions: list,
    eval_metrics: dict,
) -> bytes:
    """
    Generate a PDF report and return bytes.
    Falls back to a plaintext-based PDF if fpdf2 unavailable.
    """
    try:
        from fpdf import FPDF
        return _generate_fpdf_report(
            candidate_name, role, ats_score, hire_prob,
            cluster_label, skills, missing_skills, suggestions, eval_metrics
        )
    except ImportError:
        return _generate_simple_pdf(
            candidate_name, role, ats_score, hire_prob,
            cluster_label, skills, missing_skills, suggestions
        )


def _generate_fpdf_report(
    candidate_name, role, ats_score, hire_prob,
    cluster_label, skills, missing_skills, suggestions, eval_metrics
):
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    default_font = "Helvetica"
    font_path = os.path.join(os.path.dirname(__file__), "..", "fonts", "DejaVuSans.ttf")
    if os.path.exists(font_path):
        try:
            pdf.add_font("DejaVu", "", font_path, uni=True)
            default_font = "DejaVu"
        except Exception:
            default_font = "Helvetica"

    # ── Header ────────────────────────────────────────────
    pdf.set_fill_color(15, 17, 23)
    pdf.rect(0, 0, 210, 40, "F")

    pdf.set_font(default_font, "B", 22)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 12, "HireLens AI", ln=False, align="L")

    pdf.set_font(default_font, "", 10)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(0, 12, f"Generated: {datetime.now().strftime('%B %d, %Y')}", ln=True, align="R")

    pdf.set_font(default_font, "", 11)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(0, 6, "AI-Powered Resume Analysis Report", ln=True, align="L")

    pdf.ln(10)

    # ── Candidate Info ────────────────────────────────────
    pdf.set_font(default_font, "B", 14)
    pdf.set_text_color(30, 30, 40)
    pdf.cell(0, 8, clean_pdf_text(f"Candidate: {candidate_name or 'Anonymous'}"), ln=True)

    pdf.set_font(default_font, "", 11)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(0, 7, clean_pdf_text(f"Target Role: {role}"), ln=True)
    pdf.cell(0, 7, clean_pdf_text(f"Candidate Persona: {cluster_label or 'N/A'}"), ln=True)
    pdf.ln(5)

    # ── Score Summary ─────────────────────────────────────
    pdf.set_font(default_font, "B", 13)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 8, "Score Summary", ln=True)
    pdf.set_draw_color(124, 58, 237)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font(default_font, "", 11)
    pdf.set_text_color(30, 30, 40)
    pdf.cell(95, 8, f"ATS Score:           {ats_score:.1f}%", border=0)
    pdf.cell(95, 8, f"Hire Probability:    {hire_prob*100:.1f}%", border=0, ln=True)

    ats_verdict = "Strong Match" if ats_score >= 75 else ("Moderate Match" if ats_score >= 50 else "Low Match")
    hire_verdict = "Highly Recommended" if hire_prob >= 0.7 else ("Consider" if hire_prob >= 0.45 else "Needs Improvement")
    pdf.set_font(default_font, "I", 10)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(95, 6, clean_pdf_text(f"  ({ats_verdict})"))
    pdf.cell(95, 6, f"  ({hire_verdict})", ln=True)
    pdf.ln(5)

    # ── Skills ─────────────────────────────────────────────
    pdf.set_font(default_font, "B", 13)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 8, "Skills Detected", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font(default_font, "", 10)
    pdf.set_text_color(30, 30, 40)
    if skills:
        skill_text = clean_pdf_text(", ".join(skills[:20]))
        pdf.multi_cell(0, 6, skill_text)
    else:
        pdf.cell(0, 6, "No skills detected.", ln=True)
    pdf.ln(3)

    if missing_skills:
        pdf.set_font(default_font, "B", 11)
        pdf.set_text_color(239, 68, 68)
        pdf.cell(0, 7, "Missing Skills (for role):", ln=True)
        pdf.set_font(default_font, "", 10)
        pdf.set_text_color(107, 114, 128)
        pdf.multi_cell(0, 6, clean_pdf_text(", ".join(missing_skills)))
    pdf.ln(5)

    # ── AI Suggestions ─────────────────────────────────────
    pdf.set_font(default_font, "B", 13)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 8, "Improvement Recommendations", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    for i, s in enumerate(suggestions[:6], 1):
        pdf.set_font(default_font, "B", 11)
        pdf.set_text_color(30, 30, 40)
        pdf.cell(0, 7, clean_pdf_text(f"{i}. {s.get('title', '')}"), ln=True)
        pdf.set_font(default_font, "", 10)
        pdf.set_text_color(75, 85, 99)
        pdf.multi_cell(0, 6, clean_pdf_text(s.get("text", "")))
        pdf.ln(2)

    # ── ML Models Used ─────────────────────────────────────
    pdf.ln(3)
    pdf.set_font(default_font, "B", 13)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 8, "Models & Methodology", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font(default_font, "", 10)
    pdf.set_text_color(75, 85, 99)
    models_info = [
        "- Role Classification: Multinomial Naive Bayes with TF-IDF (1,2)-gram features",
        "- Hire Probability: Logistic Regression (L2, lbfgs solver) on engineered features",
        "- Candidate Persona: K-Means Clustering (k=4) with standardized features",
        "- Visualization: PCA (2 components) + Hierarchical Clustering (Ward linkage)",
        "- ATS Scoring: TF-IDF cosine similarity between resume and job description",
        "- NLP Pipeline: Tokenization - Stopword removal - Lemmatization",
    ]
    for line in models_info:
        pdf.cell(0, 6, clean_pdf_text(line), ln=True)

    # ── Footer ─────────────────────────────────────────────
    pdf.set_y(-25)
    pdf.set_font(default_font, "I", 9)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(
        0,
        5,
        clean_pdf_text("Generated by HireLens AI - Confidential - For recruitment purposes only"),
        align="C",
    )

    return bytes(pdf.output())


def _generate_simple_pdf(
    candidate_name, role, ats_score, hire_prob,
    cluster_label, skills, missing_skills, suggestions
):
    """Minimal text-based PDF without fpdf2."""
    lines = [
        "HireLens AI - Resume Analysis Report",
        f"Generated: {datetime.now().strftime('%B %d, %Y')}",
        "=" * 60,
        f"Candidate: {candidate_name or 'Anonymous'}",
        f"Target Role: {role}",
        f"Candidate Persona: {cluster_label or 'N/A'}",
        "",
        "SCORES",
        f"  ATS Score:        {ats_score:.1f}%",
        f"  Hire Probability: {hire_prob*100:.1f}%",
        "",
        "SKILLS DETECTED",
        ", ".join(skills[:20]) if skills else "None detected",
        "",
        "MISSING SKILLS",
        ", ".join(missing_skills) if missing_skills else "None",
        "",
        "RECOMMENDATIONS",
    ]
    for i, s in enumerate(suggestions[:6], 1):
        lines.append(f"{i}. {s.get('title','')}: {s.get('text','')}")

    content = "\n".join(lines)
    return content.encode("utf-8")
