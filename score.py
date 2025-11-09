from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load compact embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Define desired profiles (you can customize per role)
IDEAL_PROFILE = {
    "Data Analyst": [
        "python", "sql", "pandas", "data visualization", "matplotlib", "excel"
    ],
    "Machine Learning Engineer": [
        "machine learning", "scikit-learn", "tensorflow", "pytorch", "mlops"
    ],
    "Full Stack Developer": [
        "react", "javascript", "flask", "fastapi", "node.js", "docker"
    ],
    "Data Engineer": [
        "spark", "airflow", "hadoop", "aws", "gcp", "etl", "data pipeline"
    ],
}

def compute_resume_score(text: str, found_skills: set):
    """
    Compute a semantic score between resume text and ideal role skill sets.
    Returns:
        score (int), details (dict)
    """
    if not found_skills:
        return 0, {"reason": "No skills detected"}

    text_emb = model.encode(text, convert_to_tensor=True)
    details = {}
    scores = []

    # Compare with each ideal profile
    for role, skills in IDEAL_PROFILE.items():
        skill_text = ", ".join(skills)
        skill_emb = model.encode(skill_text, convert_to_tensor=True)
        sim = util.cos_sim(text_emb, skill_emb).item()
        pct = round(sim * 100, 2)
        scores.append(pct)
        details[role] = pct

    avg_score = round(float(np.mean(scores)), 2)
    best_role = max(details, key=details.get)

    return int(avg_score), {
        "role_scores": details,
        "best_fit_role": best_role,
        "reason": f"Strongest alignment with {best_role} role.",
    }

def summarize_findings(details: dict) -> str:
    best = details.get("best_fit_role", "Generalist")
    return f"Resume aligns best with **{best}** profile. Role fit scores: {details.get('role_scores', {})}"
