from Resume_extract import (
    extract_name, extract_emails, extract_phone_numbers, extract_skills,
    extract_bachelor_degrees, extract_masters_degrees, extract_experience,
    extract_marks, extract_12th_qualification, extract_10th_qualification,
    get_total_experience_from_resume,extract_experience_section,extract_durations,calculate_total_experience
)

def test_extract_emails():
    text = "Contact john.doe@example.com or jane_smith123@domain.org for details."
    expected = ["john.doe@example.com", "jane_smith123@domain.org"]
    assert extract_emails(text) == expected

    text_no_email = "No email here!"
    expected_no_email = []
    assert extract_emails(text_no_email) == expected_no_email

def test_extract_phone_numbers():
    text = "You can reach me at +91 7867676777"
    expected = ["7867676777"]
    assert extract_phone_numbers(text) == expected

    text_no_phone = "No phone number in this text."
    expected_no_phone = []
    assert extract_phone_numbers(text_no_phone) == expected_no_phone

def test_extract_skills():
    text = "I am skilled in Python."
    expected = ["python"]
    assert extract_skills(text) == expected

    text_empty_skills = "I have no skills mentioned."
    expected_empty = []
    assert extract_skills(text_empty_skills) == expected_empty

def test_extract_name():
    text = "John Doe\nLocation: New York\nContact: 555-1234"
    expected = "John Doe"
    assert extract_name(text) == expected


def test_extract_bachelor_degrees():
    text = "BTech in Computer Science and B.Sc in Mathematics."
    expected = ["Bachelor of Technology", "Bachelor of Science"]
    assert extract_bachelor_degrees(text) == expected

    text_no_bachelor = "No degree mentioned here."
    expected_no_bachelor = []
    assert extract_bachelor_degrees(text_no_bachelor) == expected_no_bachelor

def test_extract_masters_degrees():
    text = "MTech in Electrical Engineering and MSc in Physics."
    expected = ["Master of Technology", "Master of Science"]
    assert extract_masters_degrees(text) == expected

    text_no_masters = "No master's degree mentioned."
    expected_no_masters = []
    assert extract_masters_degrees(text_no_masters) == expected_no_masters

def test_extract_marks():
    text = "My CGPA is 8.5 and I scored 85% in my final exams."
    expected = ["85"]
    assert extract_marks(text) == expected

    text_no_marks = "No marks or CGPA mentioned."
    expected_no_marks = []
    assert extract_marks(text_no_marks) == expected_no_marks

def test_extract_12th_qualification():
    text = "I completed my 12th from XYZ School."
    expected = ["12th Grade"]
    assert extract_12th_qualification(text) == expected


def test_extract_10th_qualification():
    text = "I passed 10th grade with distinction."
    expected = ["10th Grade"]
    assert extract_10th_qualification(text) == expected


def test_extract_experience_section():
    text = "Experience Worked at ABC Corp as a Software Engineer.\nSkills: Python, C++"
    expected = "Worked at ABC Corp as a Software Engineer."
    assert extract_experience_section(text) == expected


def test_total_experience_with_gap():
    resume_text = """
    Experience:
    - Software Developer, Company A, November 2020 - November 2021
    - Senior Software Developer, Company B, November 2022 - November 2023
    """

    expected_output = "2 years and 0 months"

    # Calling the function to calculate total experience
    total_experience = get_total_experience_from_resume(resume_text)

    # Asserting the expected output with the actual output
    assert total_experience == expected_output