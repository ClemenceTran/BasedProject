from flask import Flask, abort, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

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
    ]
    return render_template("insight.html", results=results)


@app.route("/insight/results/<int:result_id>")
def insight_result_detail(result_id: int):
    # Fake lookup (replace with DB later)
    fake_db = {
        1: {"title": "Result 1", "summary": "This is a detailed summary for Result 1."},
        2: {"title": "Result 2", "summary": "This is a detailed summary for Result 2."},
        3: {"title": "Result 3", "summary": "This is a detailed summary for Result 3."},
    }

    data = fake_db.get(result_id)
    if not data:
        abort(404)

    return render_template("results.html", result_id=result_id, data=data)


@app.route("/talent")
def talent():
    return render_template("index.html", page="talent")


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
    # You can read mode in the template with: request.args.get("mode")
    return render_template("interview_room.html")


@app.route("/logout")
def logout():
    return redirect(url_for("signin"))


# ------------------- RUN APP -------------------
if __name__ == "__main__":
    app.run(debug=True)