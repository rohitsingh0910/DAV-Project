import pytest
from total_score import Skill, Experience, Qualification

# Test 1: Test Skill score calculation
@pytest.fixture
def skill_data():
    return Skill(
        skills=["Python", "Java", "SQL"],
        job_skills=["python", "java", "machine learning", "sql"]
    )

def test_skill_score(skill_data):
    score = skill_data.skill_score()
    assert score == 75.0  # 3 matched skills out of 4 job skills


def test_skill_score_perfect_match():
    skills = ["Python", "JavaScript", "SQL"]
    job_skills = ["python", "javascript", "sql"]
    skill = Skill(skills, job_skills)
    assert skill.skill_score() == 100

def test_skill_score_partial_match():
    skills = ["Python", "JavaScript", "SQL"]
    job_skills = ["python", "c++", "sql"]
    skill = Skill(skills, job_skills)
    assert skill.skill_score() == 66.66666666666666  # 2 out of 3 skills match

def test_skill_score_no_match():
    skills = ["Python", "JavaScript", "SQL"]
    job_skills = ["c++", "ruby", "go"]
    skill = Skill(skills, job_skills)
    assert skill.skill_score() == 0

def test_experience_score_perfect_match():
    job_experience = "3 to 5"
    year = "4 years"
    experience = Experience(job_experience, year)
    assert experience.experience_score() == 100

def test_experience_score_partial_match():
    job_experience = "3 to 5"
    year = "2 years"
    experience = Experience(job_experience, year)
    assert experience.experience_score() == 50  # Experience is within the range

def test_experience_score_below_minimum():
    job_experience = "3 to 5"
    year = "1 year"
    experience = Experience(job_experience, year)
    assert experience.experience_score() == 50  # Experience is below the minimum

def test_experience_score_no_match():
    job_experience = "3 to 5"
    year = "6 years"
    experience = Experience(job_experience, year)
    assert experience.experience_score() == 0  # Experience exceeds the range

def test_experience_score_single_experience():
    job_experience = "4"
    year = "4 years"
    experience = Experience(job_experience, year)
    assert experience.experience_score() == 100  # Experience matches p


def test_check_qualification_match():
    degree = ["B.Tech", "M.Tech"]
    job_qualification = ["B.Tech"]
    qualification = Qualification(degree, [], [80, 75, 7.5], job_qualification)
    assert qualification.check_qualification(degree, job_qualification) == ["b.tech"]

def test_check_qualification_no_match():
    degree = ["B.Sc"]
    job_qualification = ["B.Tech"]
    qualification = Qualification(degree, [], [70, 65, 7.0], job_qualification)
    assert qualification.check_qualification(degree, job_qualification) == []

def test_marks_converter_valid():
    qualification = Qualification([], [], [8.0, 7.5, 6.0], [])
    marks_10th, marks_12th, cgpa = qualification.marks_converter(8, 7, 7)
    assert marks_10th == 76.0  # 8*9.5

def test_qualification_score_below_threshold():
    degree = ["B.Sc"]
    job_qualification = ["B.Tech"]
    qualification = Qualification(degree, [], [60, 50, 5.5], job_qualification)
    assert qualification.qualification_score() == 0  # Doesn't meet the qualification criteria


def test_qualification_score_no_matching_degree():
    degree = ["Diploma"]
    job_qualification = ["B.Tech", "M.Tech"]
    qualification = Qualification(degree, [], [80, 75, 7.5], job_qualification)
    assert qualification.qualification_score() == 0  # No matching degree
