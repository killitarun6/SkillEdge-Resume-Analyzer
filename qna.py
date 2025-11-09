from typing import List, Dict, Set

_Q_TEMPLATES = {
    "python": [
        ("Explain list vs tuple in Python. When would you use each?",
         "Lists are mutable and suited for collections that change; tuples are immutable and can be used as dict keys or to enforce read-only semantics."),
        ("What are Python generators and why are they memory efficient?",
         "They yield items lazily, producing values on demand without storing the whole sequence in memory."),
    ],
    "pandas": [
        ("How do you handle missing values in pandas?",
         "Common approaches: dropna, fillna with constants or statistics, or use interpolation; choice depends on data semantics."),
    ],
    "scikit-learn": [
        ("How do you prevent data leakage in model training?",
         "Split before transform; fit scalers/encoders on train only; use Pipelines and cross-validation appropriately."),
    ],
    "tensorflow": [
        ("What is the difference between TensorFlow and Keras?",
         "Keras is a high-level API that can run on top of TensorFlow; TF provides low-level ops and the runtime."),
    ],
    "nlp": [
        ("What are word embeddings and why are they useful?",
         "Dense vector representations capturing semantic similarity; useful for downstream NLP tasks."),
    ],
    "sql": [
        ("How do you optimize a slow SQL query?",
         "Check indexes, analyze EXPLAIN plan, reduce SELECT *, filter early, and avoid unnecessary joins/subqueries."),
    ],
}

def generate_qna(found_skills: Set[str]) -> List[Dict]:
    qna: List[Dict] = []
    for skill in sorted(found_skills):
        if skill in _Q_TEMPLATES:
            for q, a in _Q_TEMPLATES[skill][:1]:  # 1 per skill to keep it concise
                qna.append({"skills": [skill], "question": q, "answer": a})
    # Fallback generic questions
    if not qna:
        qna = [
            {"skills": ["general"], "question": "Walk me through a recent project you built.",
             "answer": "Briefly outline the problem, your approach, tech stack, data, metrics, and outcome. Emphasize your impact."},
            {"skills": ["general"], "question": "How do you debug complex issues?",
             "answer": "Reproduce reliably, isolate variables, add logging, write minimal failing tests, and iterate with hypotheses."},
        ]
    return qna[:8]
