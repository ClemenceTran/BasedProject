from flask import Flask, abort, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)

# ------------------- CONFIG -------------------
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Optional: limit upload size (e.g. 10MB)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ------------------- RESULTS STORAGE (for Talent averages) -------------------
DATA_DIR = os.path.join(app.root_path, "data")
os.makedirs(DATA_DIR, exist_ok=True)
RESULTS_FILE = os.path.join(DATA_DIR, "results.json")

SKILL_KEYS = [
    ("soft_skills", "Soft Skills"),
    ("communication", "Communication"),
    ("answer_structure", "Answer Structure"),
    ("technical", "Technical"),
    ("content_relevance", "Content Relevant"),
    ("problem_solving", "Problem - Solving"),
]


def load_results():
    """
    Expected structure (later):
    [
      {"id": 1, "title": "...", "scores": {"soft_skills": 70, ...}},
      ...
    ]
    """
    if not os.path.exists(RESULTS_FILE):
        return []
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f) or []
    except Exception:
        return []


def avg_skill_scores(results):
    if not results:
        return {k: 0 for k, _ in SKILL_KEYS}

    sums = {k: 0.0 for k, _ in SKILL_KEYS}
    counts = {k: 0 for k, _ in SKILL_KEYS}

    for r in results:
        scores = r.get("scores") or {}
        for k, _ in SKILL_KEYS:
            v = scores.get(k)
            if isinstance(v, (int, float)):
                sums[k] += float(v)
                counts[k] += 1

    avgs = {}
    for k, _ in SKILL_KEYS:
        avgs[k] = round(sums[k] / counts[k]) if counts[k] else 0
        avgs[k] = max(0, min(100, avgs[k]))
    return avgs


def score_label(pct: int) -> str:
    if pct >= 80:
        return "Excellent!"
    if pct >= 65:
        return "Good!"
    if pct >= 50:
        return "Fair"
    return "Needs work"


# ------------------- AUTH ROUTES -------------------
@app.route("/", methods=["GET", "POST"])
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username_or_email = request.form.get("username")
        password = request.form.get("password")
        # TODO: validate user
        return redirect(url_for("dashboard"))
    return render_template("signin.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        # TODO: save user
        return redirect(url_for("signin"))
    return render_template("signup.html")


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        # TODO: handle password reset
        return redirect(url_for("signin"))
    return render_template("forgot_password.html")


# ------------------- DASHBOARD & PAGES -------------------
@app.route("/dashboard")
def dashboard():
    return render_template("index.html", page="dashboard")


@app.route("/insight")
def insight():
    # Fake results list (replace with DB later)
    results = [
        {"id": 1, "title": "Result 1"},
        {"id": 2, "title": "Result 2"},
        {"id": 3, "title": "Result 3"},
        {"id": 4, "title": "Result 4"},
        {"id": 5, "title": "Result 5"},
        {"id": 6, "title": "Result 6"},
        {"id": 7, "title": "Result 7"},
        {"id": 8, "title": "Result 8"},
        {"id": 9, "title": "Result 9"},
        {"id": 10, "title": "Result 10"},
        {"id": 11, "title": "Result 11"},
        {"id": 12, "title": "Result 12"},
        {"id": 13, "title": "Result 13"},
        {"id": 14, "title": "Result 14"},
    ]
    return render_template("insight.html", results=results)


@app.route("/insight/results/<int:result_id>")
def insight_result_detail(result_id):
    # Mock Data (Replace with DB later)
    data = {
        "title": "Mock Technical Interview",
        "summary": "You performed strongly overall. Communication was clear, and your technical explanations were solid. Minor improvements needed in pacing and adding measurable impact.",

        "overall_score": 82,
        "level": "Strong",
        "readiness": "75%",
        "compare": "+6% vs last attempt",

        "communication": {
            "clarity": 80,
            "confidence": 70,
            "pace": 65,
            "feedback": "You communicated clearly but spoke slightly fast during technical explanations. Try pausing after important points."
        },

        "softskills": {
            "engagement": 75,
            "structure": 70,
            "professionalism": 85,
            "feedback": "Your answers followed a logical structure. Consider adding stronger storytelling and measurable outcomes."
        },

        "content": {
            "relevance": 85,
            "depth": 75,
            "examples": 70,
            "feedback": "Your answers were relevant and technically sound. Add more real-world examples with metrics."
        },

        "questions": [
            {
                "title": "Tell me about yourself",
                "score": 78,
                "strengths": [
                    "Clear structure",
                    "Confident delivery",
                    "Relevant experience mentioned"
                ],
                "weaknesses": [
                    "Too generic introduction",
                    "Missing measurable achievements"
                ],
                "suggested_answer": "I am a software engineer with 3 years of experience building scalable web applications. In my previous role, I improved system performance by 30% by optimizing database queries and introducing caching mechanisms."
            },
            {
                "title": "Explain a challenging project",
                "score": 85,
                "strengths": [
                    "Good technical explanation",
                    "Clear problem description"
                ],
                "weaknesses": [
                    "Did not quantify impact clearly"
                ],
                "suggested_answer": "One challenging project involved redesigning a legacy API system. I led a refactor that reduced response time by 40% and improved reliability during peak traffic."
            }
        ]
    }

    return render_template("results.html", data=data)


@app.route("/talent")
def talent():
    # This now works because helpers exist
    results = load_results()
    avgs = avg_skill_scores(results)

    cards = []
    for key, title in SKILL_KEYS:
        pct = int(avgs.get(key, 0))
        cards.append({
            "key": key,
            "title": title,
            "pct": pct,
            "label": score_label(pct),
        })

    return render_template("talent.html", cards=cards, total_results=len(results))


@app.route("/profile")
def profile():
    return render_template("index.html", page="profile")


# ------------------- INTERVIEW FLOW -------------------
@app.route("/interview", methods=["GET"])
def interview():
    return render_template("interview.html", page="interview")


@app.route("/interview/step1", methods=["POST"])
def interview_step1():
    cv_file = request.files.get("cv")
    job_description = (request.form.get("job_description") or "").strip()

    if not cv_file or cv_file.filename == "":
        return {"ok": False, "error": "CV is required."}, 400

    if not allowed_file(cv_file.filename):
        return {"ok": False, "error": "Invalid file type. Use PDF/DOC/DOCX."}, 400

    if not job_description:
        return {"ok": False, "error": "Job description is required."}, 400

    filename = secure_filename(cv_file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    cv_file.save(save_path)

    return {"ok": True, "cv_filename": filename}, 200


@app.route("/interview/step2", methods=["POST"])
def interview_step2():
    interview_type = (request.form.get("interview_type") or "").strip().lower()

    if interview_type not in {"hr", "technical"}:
        return {"ok": False, "error": "Invalid interview type."}, 400

    # This becomes /interview-room?mode=hr or ?mode=technical
    return {"ok": True, "redirect": url_for("interview_room", mode=interview_type)}, 200


@app.route("/interview-room")
def interview_room():
    return render_template("interview_room.html")


@app.route("/logout")
def logout():
    return redirect(url_for("signin"))


# ------------------- RUN APP -------------------
if __name__ == "__main__":
    app.run(debug=True)