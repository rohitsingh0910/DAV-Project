from flask import Flask, render_template, request, flash, redirect, url_for,session,jsonify
from werkzeug.utils import secure_filename
from recommend import fetch_youtube_videos
from flask_paginate import Pagination, get_page_parameter
from models import init_db, db, User, SavedResume
from extract import extract_text
from Resume_extract import (
    extract_name, extract_emails, extract_phone_numbers, extract_skills,
    extract_bachelor_degrees, extract_masters_degrees,
    extract_marks, extract_12th_qualification, extract_10th_qualification,
    get_total_experience_from_resume
)
from Jobdescription_extract import extract_skills_role_experience_qualification
from total_score import Skill, Experience, Qualification
from concurrent.futures import ThreadPoolExecutor
import os

app = Flask(__name__)
app.secret_key = 'neha'

# Upload configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}
MAX_FILE_COUNT = 100000  # Maximum number of resume files allowed per upload
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app)

# Helper function to check valid file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('home.html')

def process_resume(resume_file, job_skills, job_role, job_experience, job_qualification):
    filename = secure_filename(resume_file.filename)
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resume_file.save(resume_path)

    try:
        resume_text = extract_text(resume_path)
    except Exception as e:
        print(f"Error extracting text from resume: {e}")
        return []

    # Extract data from the resume
    name = extract_name(resume_text)
    emails = extract_emails(resume_text)
    phone_numbers = extract_phone_numbers(resume_text)
    skills = extract_skills(resume_text)
    bachelor_degree = extract_bachelor_degrees(resume_text)
    masters_degree = extract_masters_degrees(resume_text)
    marks = extract_marks(resume_text)
    _12th = extract_12th_qualification(resume_text)
    _10th = extract_10th_qualification(resume_text)
    year = get_total_experience_from_resume(resume_text)

    # Calculate the total score
    skill_s = Skill(skills, job_skills)
    experience_s = Experience(job_experience, year)
    qualification_s = Qualification(bachelor_degree, masters_degree, marks, job_qualification)
    if skill_s.skill_score() > 0.0:
        exp = experience_s.experience_score()
    else:
        exp = 0

    total_score = (
        (skill_s.skill_score() * 0.50) +
        (exp * 0.30) +
        (qualification_s.qualification_score() * 0.20)
    )

    return [{
        'name': name.title(),
        'emails': emails[0],
        'phone_numbers': phone_numbers[0],
        'skills': skills,
        'bachelor_degree': bachelor_degree,
        'marks': marks,
        '12th': _12th,
        '10th': _10th,
        'masters_degree': masters_degree,
        'total_experience': year,
        'job_skills': job_skills,
        'job_role': job_role,
        'job_experience': job_experience,
        'job_qualification': job_qualification,
        'total_score': total_score
    }]

@app.route('/user_resume', methods=['GET', 'POST'])
def user_resume():
    if request.method == 'POST':
        resume_file = request.files.get('resume')
        job_description_file = request.files.get('job_description')

        if not resume_file or not job_description_file:
            flash("Please upload both resume and job description files.")
            return redirect(request.url)

        job_description_filename = secure_filename(job_description_file.filename)
        job_description_path = os.path.join(app.config['UPLOAD_FOLDER'], job_description_filename)
        job_description_file.save(job_description_path)

        try:
            job_description_text = extract_text(job_description_path)
        except Exception as e:
            flash(f"Error extracting text from job description: {e}")
            return redirect(request.url)

        job_skills, job_role, job_experience, job_qualification = extract_skills_role_experience_qualification(job_description_text)
        result = process_resume(resume_file, job_skills, job_role, job_experience, job_qualification)

        unmatched_skills = [skill for skill in job_skills if skill.lower() not in [s.lower() for s in result[0]['skills']]]
        suggested_courses = {skill: fetch_youtube_videos(skill) for skill in unmatched_skills}

        return render_template('user_results.html', result=result[0], suggested_courses=suggested_courses)

    return render_template('user_resume.html')

@app.route('/recruiter', methods=['GET', 'POST'])
def recruiter():
    if 'username' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))  # Redirect to login if not logged in

    recruiter_name = session['username']  # Fetch from session

    if request.method == 'POST':
        if 'resume' not in request.files or 'job_description' not in request.files:
            flash("No files part")
            return redirect(request.url)

        resume_files = request.files.getlist('resume')
        job_description_file = request.files.get('job_description')

        if not job_description_file or not allowed_file(job_description_file.filename):
            flash("Please upload a valid job description file (PDF or DOCX).")
            return redirect(request.url)

        if len(resume_files) > MAX_FILE_COUNT:
            flash(f"Please upload no more than {MAX_FILE_COUNT} resume files at a time.")
            return redirect(request.url)

        resume_files = [file for file in resume_files if allowed_file(file.filename)]

        if not resume_files:
            flash("Please upload valid resume files (PDF or DOCX).")
            return redirect(request.url)

        job_description_filename = secure_filename(job_description_file.filename)
        job_description_path = os.path.join(app.config['UPLOAD_FOLDER'], job_description_filename)
        job_description_file.save(job_description_path)

        try:
            job_description_text = extract_text(job_description_path)
        except Exception as e:
            flash(f"Error extracting text from job description: {e}")
            return redirect(request.url)

        job_skills, job_role, job_experience, job_qualification = extract_skills_role_experience_qualification(job_description_text)

        results = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_resume, resume_file, job_skills, job_role, job_experience, job_qualification) for resume_file in resume_files]
            for future in futures:
                try:
                    results.extend(future.result())
                except Exception as e:
                    flash(f"Error processing file: {e}")
                    continue

        sorted_results = sorted(results, key=lambda x: x['total_score'], reverse=True)

        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = 30
        total = len(sorted_results)
        paginated_results = sorted_results[(page - 1) * per_page: page * per_page]
        pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')

        return render_template('results.html', results=paginated_results, pagination=pagination, recruiter_name=recruiter_name)

    return render_template('upload_form.html', recruiter_name=recruiter_name)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('signup.html', error="Email already exists")

        new_user = User(name=fullname, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(name=username).first()

        if user and user.password == password:
            session['username'] = username  # Store in session
            return redirect(url_for('recruiter'))  # Redirect without passing manually
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

@app.route('/save_resume', methods=['POST'])  # Only POST is needed
def save_resume():
    if 'username' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))

    recruiter_name = session['username']
    candidate_name = request.form.get('candidate_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    skills = request.form.get('skills')
    experience = request.form.get('experience')
    qualification = request.form.get('qualification')
    total_score = request.form.get('total_score')

    new_resume = SavedResume(
        recruiter_name=recruiter_name,
        candidate_name=candidate_name,
        email=email,
        phone=phone,
        skills=skills,
        experience=experience,
        qualification=qualification,
        total_score=total_score
    )
    db.session.add(new_resume)
    db.session.commit()

    flash("Resume saved successfully!", "success")

    # Fetch updated results to stay on the same page
    results = SavedResume()  # Replace with actual query fetching resumes
    return render_template('results.html', results=results, recruiter_name=recruiter_name)


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)