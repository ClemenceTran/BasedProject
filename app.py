from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# ------------------- CONFIG -------------------
# Folder to store uploaded CV files
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
def login():
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
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        # TODO: handle password reset
        return redirect(url_for("login"))
    return render_template("forgot_password.html")


# ------------------- DASHBOARD & PAGES -------------------
@app.route("/dashboard")
def dashboard():
    return render_template("index.html", page="dashboard")


@app.route("/insight")
def insight():
    return render_template("index.html", page="insight")


@app.route("/talent")
def talent():
    return render_template("index.html", page="talent")


@app.route("/profile")
def profile():
    return render_template("index.html", page="profile")


# ------------------- INTERVIEW FLOW -------------------
# STEP 1+2 are inside interview.html (handled by JS), Step 3 is another page.

@app.route("/interview", methods=["GET"])
def interview():
    # single page that contains Step 1 and Step 2 (client-side)
    return render_template("interview.html", page="interview")


@app.route("/interview/step1", methods=["POST"])
def interview_step1():
    """
    Receives:
      - cv (file)
      - job_description (text)
    Saves CV to /uploads and then redirects to /interview?step=2 (optional) or returns OK.
    Since your UI is JS-based steps, we just return success JSON or redirect.
    """
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

    # TODO: store/save job_description somewhere (db, session, file, etc.)
    # Example: session["job_description"] = job_description  (requires secret_key + sessions)

    return {"ok": True, "cv_filename": filename}, 200


@app.route("/interview/step2", methods=["POST"])
def interview_step2():
    """
    Receives:
      - interview_type: "hr" or "technical"
    Redirects to interview room with mode in query string.
    """
    interview_type = (request.form.get("interview_type") or "").strip().lower()

    if interview_type not in {"hr", "technical"}:
        return {"ok": False, "error": "Invalid interview type."}, 400

    # TODO: store interview_type somewhere if needed (session/db)

    return {"ok": True, "redirect": url_for("interview_room", mode=interview_type)}, 200


@app.route("/interview-room")
def interview_room():
    return render_template("interview_room.html")


@app.route("/logout")
def logout():
    # TODO: clear session if you use it later
    return redirect(url_for("login"))
# ------------------- RUN APP -------------------
if __name__ == "__main__":
    app.run(debug=True)