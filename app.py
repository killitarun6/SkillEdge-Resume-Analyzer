import streamlit as st
from pathlib import Path
import json
import yaml
from modules.extract import extract_text
from modules.skills import extract_skills, canonical_skillset
from modules.score import compute_resume_score, summarize_findings
from modules.jobs import recommend_jobs
from modules.qna import generate_qna

APP_TITLE = "Skill Edge: Resume Analyzer (Streamlit)"
DATA_DIR = Path("data_store")
DATA_DIR.mkdir(exist_ok=True)

# ---------------------- Auth utils ----------------------
def load_users():
    try:
        with open("users.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f).get("users", [])
    except Exception:
        return []

def check_credentials(username, password):
    for u in load_users():
        if u.get("username") == username and u.get("password") == password:
            return True
    return False

def require_login():
    if "auth" not in st.session_state:
        st.session_state.auth = {"logged_in": False, "user": None}

    if st.session_state.auth["logged_in"]:
        return True

    st.title(APP_TITLE)
    st.subheader("Login")
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
    if submitted:
        if check_credentials(username, password):
            st.session_state.auth["logged_in"] = True
            st.session_state.auth["user"] = username
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid credentials.")
    st.stop()

# ---------------------- Persistence ----------------------
def user_file(user: str) -> Path:
    return DATA_DIR / f"{user}.json"

def save_user_result(user: str, payload: dict):
    fp = user_file(user)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def load_user_result(user: str):
    fp = user_file(user)
    if fp.exists():
        with open(fp, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# ---------------------- UI Layout ----------------------
def sidebar():
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Go to",
            ["Upload Resume", "Results Dashboard", "Interview Q&A", "About"],
            index=0,
        )
        if st.button("Logout"):
            st.session_state.auth = {"logged_in": False, "user": None}
            st.rerun()
    return page

# ---------------------- Pages ----------------------
def page_upload(user: str):
    st.title("📤 Upload Your Resume")
    st.caption("Accepted formats: PDF, DOCX")

    uploaded = st.file_uploader("Choose a file", type=["pdf", "docx"])
    analyze = st.button("Analyze Resume", type="primary", use_container_width=True)

    if analyze and not uploaded:
        st.warning("Please upload a PDF or DOCX file first.")
        return

    if uploaded and analyze:
        with st.spinner("Extracting text..."):
            text = extract_text(uploaded)

        if not text or len(text.strip()) < 50:
            st.error("Sorry, we couldn't extract enough text from the document.")
            return

        with st.spinner("Mining skills and computing score..."):
            skills_found = extract_skills(text)
            score, details = compute_resume_score(text, skills_found)
            summary = summarize_findings(details)
            jobs = recommend_jobs(skills_found)
            qna = generate_qna(skills_found)

        result = {
            "summary": summary,
            "score": score,
            "skills_found": sorted(list(skills_found)),
            "missing_skills": sorted(list(details.get("missing_skills", []))),
            "good_skills": sorted(list(details.get("good_skills", []))),
            "jobs": jobs,
            "qna": qna,
        }
        save_user_result(user, result)
        st.success("Analysis completed and saved. Open the Results Dashboard.")
        with st.expander("Preview extracted text (first 1200 chars)"):
            st.write(text[:1200] + ("..." if len(text) > 1200 else ""))

def page_results(user: str):
    st.title("📊 Results Dashboard")
    result = load_user_result(user)
    if not result:
        st.info("No results yet. Please analyze a resume first in 'Upload Resume'.")
        return

    st.metric("Resume Score", f"{result['score']} / 100")
    st.write(result["summary"])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Detected Skills")
        if result["skills_found"]:
            st.write(", ".join(result["skills_found"]))
        else:
            st.write("—")

    with col2:
        st.subheader("Missing / Recommended Skills")
        if result["missing_skills"]:
            st.write(", ".join(result["missing_skills"]))
        else:
            st.write("Looks good! No critical gaps detected.")

    st.subheader("💼 Job Recommendations")
    for j in result["jobs"]:
        st.markdown(f"- **{j['title']}**  — match: {j['match']}%  \n  *{j['why']}*")

def page_qna(user: str):
    st.title("🧠 AI-Powered Interview Q&A (Template)")
    result = load_user_result(user)
    if not result:
        st.info("No analysis found. Please analyze a resume first.")
        return

    st.caption("These are template questions generated from your skills. You can expand and practice:")
    for i, item in enumerate(result["qna"], start=1):
        with st.expander(f"Q{i}. {item['question']}"):
            st.write(item["answer"])
            st.caption(f"Skill focus: {', '.join(item['skills'])}")

def page_about():
    st.title("ℹ️ About This Demo")
    st.write(
        """
        This Streamlit app demonstrates the 'Skill Edge: Resume Analyzer' UI:
        - Upload PDF/DOCX → Extract text
        - Skill mining vs a canonical skill set
        - Heuristic scoring (0–100)
        - Job suggestions
        - Interview Q&A templates

        Replace heuristics with your NLP models or API endpoints as you grow.
        """
    )
    st.subheader("Built-in Skill Universe")
    st.code(", ".join(sorted(canonical_skillset())), language="text")

# ---------------------- Main App ----------------------
def main():
    require_login()
    user = st.session_state.auth["user"]
    st.sidebar.success(f"Logged in as: {user}")
    page = sidebar()

    if page == "Upload Resume":
        page_upload(user)
    elif page == "Results Dashboard":
        page_results(user)
    elif page == "Interview Q&A":
        page_qna(user)
    else:
        page_about()

if __name__ == "__main__":
    st.set_page_config(page_title=APP_TITLE, page_icon="🧩", layout="wide")
    main()
