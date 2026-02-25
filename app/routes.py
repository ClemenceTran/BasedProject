import os
import json
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session

routes_bp = Blueprint("routes", __name__)

# ---------------- Login required ----------------
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("auth.signin"))
        return fn(*args, **kwargs)
    return wrapper


# ---------------- Results storage (Talent) ----------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
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


# ---------------- Home ----------------
@routes_bp.route("/", endpoint="home")
def home():
    # if logged in -> go interview, else -> signin
    if "user" in session:
        return redirect(url_for("interview.interview"))
    return redirect(url_for("auth.signin"))


# ---------------- Insight ----------------
@routes_bp.route("/insight", endpoint="insight")
@login_required
def insight():
    results = [
        {"id": 1, "title": "Result 1"},
        {"id": 2, "title": "Result 2"},
        {"id": 3, "title": "Result 3"},
        {"id": 4, "title": "Result 4"},
    ]
    return render_template("insight.html", results=results)


@routes_bp.route("/insight/results/<int:result_id>", endpoint="insight_result_detail")
@login_required
def insight_result_detail(result_id):
    # Keep your mock data for now (later replace with DB)
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
        "questions": []
    }
    return render_template("results.html", data=data)


# ---------------- Talent ----------------
@routes_bp.route("/talent", endpoint="talent")
@login_required
def talent():
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


# ---------------- Profile ----------------
@routes_bp.route("/profile", endpoint="profile")
@login_required
def profile():
    # You can later load from DB/users.json
    user = {
        "name": "Clemence",
        "surname": "Tran",
        "username": session.get("user"),
        "email": "clemence@example.com",
        "created_at": "2026-02-20",
    }
    return render_template("profile.html", user=user)


@routes_bp.route("/profile/update", methods=["POST"], endpoint="update_profile")
@login_required
def update_profile():
    name = (request.form.get("name") or "").strip()
    surname = (request.form.get("surname") or "").strip()

    user = {
        "name": name,
        "surname": surname,
        "username": session.get("user"),
        "email": "clemence@example.com",
        "created_at": "2026-02-20",
    }

    return render_template("profile.html", user=user, status="ok", message="Information updated.")


@routes_bp.route("/change-password", methods=["POST"], endpoint="change_password")
@login_required
def change_password():
    new_password = request.form.get("new_password") or ""
    confirm_password = request.form.get("confirm_password") or ""

    user = {
        "name": "Clemence",
        "surname": "Tran",
        "username": session.get("user"),
        "email": "clemence@example.com",
        "created_at": "2026-02-20",
        "plan": "Free",
    }

    if new_password != confirm_password:
        return render_template("profile.html", user=user, status="err", message="New passwords do not match.")

    if len(new_password) < 6:
        return render_template("profile.html", user=user, status="err", message="Password must be at least 6 characters.")

    # later: update users.json / DB
    return render_template("profile.html", user=user, status="ok", message="Password updated successfully.")