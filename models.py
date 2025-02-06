
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class SavedResume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recruiter_name = db.Column(db.String(100), nullable=False)  # Recruiter who saved the resume
    candidate_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    skills = db.Column(db.Text, nullable=False)
    experience = db.Column(db.String(50), nullable=True)
    qualification = db.Column(db.String(100), nullable=True)
    total_score = db.Column(db.Float, nullable=False)

    def __init__(self, recruiter_name, candidate_name, email, phone, skills, experience, qualification, total_score):
        self.recruiter_name = recruiter_name
        self.candidate_name = candidate_name
        self.email = email
        self.phone = phone
        self.skills = skills
        self.experience = experience
        self.qualification = qualification
        self.total_score = total_score

def init_db():
    # Creates all the tables
    db.create_all()