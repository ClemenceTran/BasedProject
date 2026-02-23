from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

# ------------------- INTERVIEW PAGE -------------------
@app.route("/interview", methods=["GET"])
def interview():
    step = int(request.args.get("step", 1))
    interview_type = request.args.get("type")  
    return render_template("index.html", page="interview", step=step, interview_type=interview_type)

@app.route("/interview/start", methods=["POST"])
def interview_start():
    interview_type = request.form.get("interview_type")
    job_description = request.form.get("job_description", "")
    cv_file = request.files.get("cv")

    return redirect(url_for("interview_room"))


@app.route("/interview-room")
def interview_room():
    return render_template("interview_room.html")

@app.route("/insight")
def insight():
    return render_template("index.html", page="insight")


@app.route("/talent")
def talent():
    return render_template("index.html", page="talent")


@app.route("/profile")
def profile():
    return render_template("index.html", page="profile")


# ------------------- RUN APP -------------------
if __name__ == "__main__":
    app.run(debug=True)
