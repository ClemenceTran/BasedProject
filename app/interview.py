import os
from functools import wraps
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

interview_bp = Blueprint("interview", __name__)

# -------- Upload config --------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -------- Login protection --------
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("auth.signin"))
        return fn(*args, **kwargs)
    return wrapper


# -------- Pages --------
@interview_bp.route("/interview", methods=["GET"])
@login_required
def interview():
    return render_template("interview.html")


@interview_bp.route("/interview-room", methods=["GET"])
@login_required
def interview_room():
    mode = (request.args.get("mode") or "hr").lower()
    if mode not in {"hr", "technical"}:
        mode = "hr"

    session["interview_mode"] = mode
    return render_template("interview_room.html")


@interview_bp.route("/interview/step1", methods=["POST"])
@login_required
def interview_step1():
    cv_file = request.files.get("cv")
    job_description = (request.form.get("job_description") or "").strip()

    if not cv_file or cv_file.filename == "":
        return jsonify(ok=False, error="CV is required."), 400

    if not allowed_file(cv_file.filename):
        return jsonify(ok=False, error="Invalid file type. Use PDF/DOC/DOCX."), 400

    if not job_description:
        return jsonify(ok=False, error="Job description is required."), 400

    filename = secure_filename(cv_file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    cv_file.save(save_path)

    session["cv_filename"] = filename
    session["job_description"] = job_description

    return jsonify(ok=True, cv_filename=filename), 200


@interview_bp.route("/interview/step2", methods=["POST"])
@login_required
def interview_step2():
    interview_type = (request.form.get("interview_type") or "").strip().lower()

    if interview_type not in {"hr", "technical"}:
        return jsonify(ok=False, error="Please select HR or Technical."), 400

    session["interview_mode"] = interview_type

    return jsonify(ok=True, redirect=url_for("interview.interview_room", mode=interview_type)), 200