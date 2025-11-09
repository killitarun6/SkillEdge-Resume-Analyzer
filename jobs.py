from typing import List, Dict, Set

# Very small, illustrative rule base
_JOB_TEMPLATES = [
    {
        "title": "Data Analyst (Python + SQL)",
        "skills": {"python", "pandas", "sql", "matplotlib"},
        "why": "Strong fit if you have Python, SQL and basic data viz.",
    },
    {
        "title": "Machine Learning Engineer",
        "skills": {"python", "scikit-learn", "tensorflow", "pytorch", "mlops"},
        "why": "Match improves with ML frameworks and MLOps exposure.",
    },
    {
        "title": "NLP Engineer",
        "skills": {"python", "nlp", "spacy", "transformers", "bert"},
        "why": "Ideal for resumes with solid NLP toolchain skills.",
    },
    {
        "title": "Data Engineer",
        "skills": {"python", "spark", "airflow", "aws", "gcp", "docker"},
        "why": "Good alignment for data pipelines and cloud experience.",
    },
    {
        "title": "Full-Stack (ML Apps)",
        "skills": {"python", "flask", "fastapi", "react", "docker"},
        "why": "Build end-to-end ML apps with APIs and simple UIs.",
    },
]

def _pct_match(found: Set[str], wanted: Set[str]) -> int:
    if not wanted:
        return 0
    return int(round(100 * len(found & wanted) / len(wanted)))

def recommend_jobs(found_skills: Set[str]) -> List[Dict]:
    recs = []
    for j in _JOB_TEMPLATES:
        recs.append({
            "title": j["title"],
            "match": _pct_match(found_skills, j["skills"]),
            "why": j["why"],
        })
    # Sort by best match first
    recs.sort(key=lambda x: x["match"], reverse=True)
    return recs[:5]
