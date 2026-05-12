from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    year = db.Column(db.String(20))
    major = db.Column(db.String(100), default="")
    bio = db.Column(db.Text, default="")
    neighborhood = db.Column(db.String(100), default="")

    sleep_schedule = db.Column(db.String(20), default="")
    cleanliness = db.Column(db.Integer, default=3)
    noise_tolerance = db.Column(db.Integer, default=3)
    guests_ok = db.Column(db.Boolean, default=True)
    smoking_ok = db.Column(db.Boolean, default=False)

    move_in = db.Column(db.String(50), default="")
    budget_min = db.Column(db.Integer, default=0)
    budget_max = db.Column(db.Integer, default=0)

    profile_complete = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
