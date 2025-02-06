import pytest
from Jobdescription_extract import ResumeExtractor


# Assuming your classes (TextExtractor, SkillsExtractor, RoleExtractor, etc.) are already defined as in your initial code

@pytest.fixture
def extractor():
    return ResumeExtractor()

def test_valid_skills(extractor):
    text = "I have experience with Python, Linux, and Machine Learning."
    skills, role, years_of_experience, qualification = extractor.extract_details(text)
    assert skills == ['linux', 'machine learning', 'python']

def test_valid_role(extractor):
    text = "Job Role: Software Engineer"
    skills, role, years_of_experience, qualification = extractor.extract_details(text)
    assert role == "Software Engineer"

def test_valid_experience(extractor):
    text = "I have 3 years of experience in Python."
    skills, role, years_of_experience, qualification = extractor.extract_details(text)
    assert years_of_experience == "3 "

def test_valid_qualification(extractor):
    text = "My qualification is B.Tech in Computer Science."
    skills, role, years_of_experience, qualification = extractor.extract_details(text)
    assert qualification == ['B.Tech']


def test_no_skills_found(extractor):
    text = "This resume doesn't mention any specific skills."
    skills, role, years_of_experience, qualification = extractor.extract_details(text)
    assert skills == []

def test_role_not_found(extractor):
    text = "This resume doesn't mention a job title."
    skills, role, years_of_experience, qualification = extractor.extract_details(text)
    assert role == "Not found"

def test_experience_not_found(extractor):
    text = "This resume doesn't mention any experience."
    skills, role, years_of_experience, qualification = extractor.extract_details(text)
    assert years_of_experience == "Not found"

def test_qualification_not_found(extractor):
    text = "This resume doesn't mention any qualifications."
    skills, role, years_of_experience, qualification = extractor.extract_details(text)
    assert qualification == []


