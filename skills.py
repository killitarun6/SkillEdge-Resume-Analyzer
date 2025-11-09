import re
import spacy

# Load lightweight English model
nlp = spacy.load("en_core_web_sm")

# Canonical technical skill set (expand as needed)
CANONICAL_SKILLS = {
    "python", "java", "c++", "c", "javascript", "typescript",
    "sql", "nosql", "pandas", "numpy", "scikit-learn", "tensorflow", "keras",
    "pytorch", "spacy", "nltk", "react", "flask", "django", "fastapi",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "linux",
    "machine learning", "deep learning", "data analysis", "data visualization",
    "html", "css", "powerbi", "tableau", "spark", "hadoop", "nlp",
}

ALIASES = {
    r"\bjs\b": "javascript",
    r"\bpy\-?torch\b": "pytorch",
    r"\bsklearn\b": "scikit-learn",
    r"\bgoogle cloud\b": "gcp",
    r"\bms\s*excel\b": "excel",
    r"\breactjs\b": "react",
    r"\bnodejs\b": "node.js",
}

def normalize_text(text: str) -> str:
    text = text.lower()
    for pat, repl in ALIASES.items():
        text = re.sub(pat, repl, text)
    return text

def extract_skills(text: str):
    """
    Hybrid extractor: combines NER + keyword matching + normalization
    """
    text = normalize_text(text)
    doc = nlp(text)

    found = set()

    # 1️⃣ Extract using NER entities
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "LANGUAGE", "SKILL"]:
            found.add(ent.text.lower())

    # 2️⃣ Keyword-based extraction
    for skill in CANONICAL_SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.add(skill.lower())

    # 3️⃣ Clean & return
    found = {s.strip() for s in found if len(s) > 2}
    return found

def canonical_skillset():
    """Return the reference list of all known skills"""
    return sorted(CANONICAL_SKILLS)