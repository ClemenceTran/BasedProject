import os
import json
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# ---------------- DATA FILES ----------------
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
USERS_FILE = os.path.join(DATA_DIR, "users.json")
RESET_FILE = os.path.join(DATA_DIR, "reset_tokens.json")

os.makedirs(DATA_DIR, exist_ok=True)


def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f) or []
    except Exception:
        return []


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def find_user(username_or_email):
    key = (username_or_email or "").strip().lower()
    for u in load_users():
        if u.get("username", "").lower() == key or u.get("email", "").lower() == key:
            return u
    return None


def load_resets():
    if not os.path.exists(RESET_FILE):
        return []
    try:
        with open(RESET_FILE, "r", encoding="utf-8") as f:
            return json.load(f) or []
    except Exception:
        return []


def save_resets(items):
    with open(RESET_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)


def find_reset(token):
    for r in load_resets():
        if r.get("token") == token:
            return r
    return None


# ---------------- ROUTES ----------------

@auth_bp.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip().lower()
        password = request.form.get("password") or ""

        if not username or not password:
            return render_template("signin.html", error="Please fill in all fields.")

        user = find_user(username)
        if not user:
            return render_template("signin.html", error="User not found.")

        if not check_password_hash(user["password_hash"], password):
            return render_template("signin.html", error="Wrong password.")

        session["user"] = user["username"]
        return redirect(url_for("routes.interview"))

    return render_template("signin.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip().lower()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not username or not email or not password:
            return render_template("signup.html", error="Please fill in all fields.")

        users = load_users()

        for u in users:
            if u["username"] == username:
                return render_template("signup.html", error="Username already exists.")
            if u["email"] == email:
                return render_template("signup.html", error="Email already exists.")

        users.append({
            "id": uuid.uuid4().hex,
            "username": username,
            "email": email,
            "password_hash": generate_password_hash(password, method="pbkdf2:sha256"),
            "created_at": datetime.utcnow().isoformat()
        })

        save_users(users)
        return redirect(url_for("auth.signin"))

    return render_template("signup.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.signin"))


# ✅ Forgot password: create token + show demo link
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()

        # security: always show same message
        msg = "Enter your email"

        if email:
            user = find_user(email)
            if user:
                token = uuid.uuid4().hex
                resets = load_resets()
                resets.append({
                    "token": token,
                    "username": user["username"],
                    "created_at": datetime.utcnow().isoformat(),
                    "used": False
                })
                save_resets(resets)

                demo_link = url_for("auth.reset_password", token=token)
                return render_template("forgot_password.html", success=msg, demo_link=demo_link)

        return render_template("forgot_password.html", success=msg)

    return render_template("forgot_password.html")


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    reset = find_reset(token)
    if not reset or reset.get("used"):
        return render_template("forgot_password.html", error="Reset link is invalid or expired.")

    if request.method == "POST":
        new_password = request.form.get("new_password") or ""
        confirm_password = request.form.get("confirm_password") or ""

        if len(new_password) < 6:
            return render_template("reset_password.html", error="Password must be at least 6 characters.", token=token)

        if new_password != confirm_password:
            return render_template("reset_password.html", error="Passwords do not match.", token=token)

        # update user password
        users = load_users()
        for u in users:
            if u["username"] == reset["username"]:
                u["password_hash"] = generate_password_hash(new_password, method="pbkdf2:sha256")
                break
        save_users(users)

        # mark token used
        resets = load_resets()
        for r in resets:
            if r.get("token") == token:
                r["used"] = True
                break
        save_resets(resets)

        return redirect(url_for("auth.signin"))

    return render_template("reset_password.html", token=token)