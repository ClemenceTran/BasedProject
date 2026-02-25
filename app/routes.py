from flask import Blueprint, render_template, redirect, url_for

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/", methods=["GET"], endpoint="home")
def home():
    return redirect(url_for("signin"))

@routes_bp.route("/signin", methods=["GET"], endpoint="signin")
def signin():
    return render_template("signin.html")

@routes_bp.route("/signup", methods=["GET"], endpoint="signup")
def signup():
    return render_template("signup.html")

@routes_bp.route("/forgot-password", methods=["GET"], endpoint="forgot_password")
def forgot_password():
    return render_template("forgot_password.html")