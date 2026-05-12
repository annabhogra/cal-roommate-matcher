import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User
from matching import rank_matches, pct

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-in-prod")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///roommates.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


def current_user():
    if "user_id" in session:
        return User.query.get(session["user_id"])
    return None


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("matches"))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        if not email.endswith("@berkeley.edu"):
            flash("Please use your @berkeley.edu email.")
            return render_template("register.html")
        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.")
            return render_template("register.html")

        user = User(
            name=request.form["name"].strip(),
            email=email,
            year=request.form["year"],
            major=request.form.get("major", "").strip(),
        )
        user.set_password(request.form["password"])
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return redirect(url_for("edit_profile"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"].strip().lower()).first()
        if user and user.check_password(request.form["password"]):
            session["user_id"] = user.id
            return redirect(url_for("matches"))
        flash("Incorrect email or password.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        user.bio = request.form.get("bio", "").strip()
        user.neighborhood = request.form.get("neighborhood", "")
        user.sleep_schedule = request.form.get("sleep_schedule", "")
        user.cleanliness = int(request.form.get("cleanliness", 3))
        user.noise_tolerance = int(request.form.get("noise_tolerance", 3))
        user.guests_ok = request.form.get("guests_ok") == "yes"
        user.smoking_ok = request.form.get("smoking_ok") == "yes"
        user.move_in = request.form.get("move_in", "")
        user.budget_min = int(request.form.get("budget_min") or 0)
        user.budget_max = int(request.form.get("budget_max") or 0)
        user.profile_complete = True
        db.session.commit()
        flash("Profile updated.")
        return redirect(url_for("matches"))

    return render_template("edit_profile.html", user=user)


@app.route("/matches")
def matches():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    others = User.query.filter(User.id != user.id, User.profile_complete == True).all()
    ranked = [(other, pct(score)) for other, score in rank_matches(user, others)]

    return render_template("matches.html", user=user, matches=ranked)


@app.route("/profile/<int:user_id>")
def profile(user_id):
    if not current_user():
        return redirect(url_for("login"))
    target = User.query.get_or_404(user_id)
    return render_template("profile.html", target=target)


if __name__ == "__main__":
    app.run(debug=True)
