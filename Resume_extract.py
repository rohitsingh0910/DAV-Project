import re
from datetime import datetime
from typing import List, Tuple
def extract_emails(text):
    email_pattern = r"[a-zA-Z0-9_%+-.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(email_pattern, text)


def extract_phone_numbers(text):
    phone_pattern = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    return re.findall(phone_pattern, text)



def extract_skills(text):
    skills_pattern = r"\b(python|linux|microcontrollers|c++|embedded c|c|Communication Protocol|java|c\+\+|data science|machine learning|sql|r|excel|spring|html|css|javascript|go|ruby|GPIO|I2C|SPI|UART|CAN|ARM|AVR|PIC|RTOS|FreeRTOS|C/C++|I2C/SPI/UART|GDB|OpenOCD|JTAG debuggers|TCP/IP|UDP|MQTT|HTTP|html|css|javascript|typescript|react|angular|vue.js|node.js|spring|django|flask|ruby|go|rust|kotlin|swift|dart|flutter|tensorflow|pytorch|deep learning|data science|nlp|big data|hadoop|spark|kafka|docker|kubernetes|aws|azure|gcp|git|ci/cd|devops|microservices|rest api|graphql|gdb|assembly|vhdl|verilog|fpga|matlab|simulink)\b"
    skills = re.findall(skills_pattern, text, re.IGNORECASE)
    skills_found = list(set([skill.lower() for skill in skills if skill.lower() not in ['r', 'following']]))
    return skills_found


def extract_experience(text):
    experience_pattern = r"(\d+)\s*(years|month[s]?)\s*(experience|exp)"
    return re.findall(experience_pattern, text)


def extract_name(text):
    lines = text.split('\n')
    name = lines[0]
    return name


def extract_bachelor_degrees(text):
    # Define the full names of the degrees
    bachelor_degrees = {
        "Bachelor of Technology": ["BTech", "B.Tech", "BTech.", "B.TECH", "BTech", "b. tech ",
                                   "Bachelor of Technology "],
        "Bachelor of Engineering": ["BE", "B.E.", "B.E", "BEng", "B.Eng", "Bachelor of Engineering"],
        "Bachelor of Science": ["BSc", "B.Sc", "BSc.", "B.Sc.", "B.Sci", "B.S.", "Bachelor of Science"],
        "Bachelor of Arts": ["BA", "B.A.", "B.A", "BArt", "B.Ars", "Bachelor of Arts"],
        "Bachelor of Commerce": ["BCom", "B.Com", "BCom.", "B.Com.", "Bachelor of Commerce"],
        "Bachelor of Design": ["BDes", "B.Des", "Bachelor of Design"],
        "Bachelor of Architecture": ["BArch", "B.Arch", "Bachelor of Architecture"],
        "Bachelor of Education": ["BEd", "B.Ed", "B.Ed.", "Bachelor of Education"],
        "Bachelor of Fine Arts": ["BFA", "B.F.A.", "B.F.A", "Bachelor of Fine Arts"],
        "Bachelor of Business Administration": ["BBA", "B.B.A.", "Bachelor of Business Administration"],
        "Bachelor of Computer Applications": ["BCA", "B.C.A.", "Bachelor of Computer Applications"]
    }

    # List to store the found degree names
    degrees_found = []

    # Iterate through the dictionary and check if any abbreviation or full name is found
    for full_name, abbreviations in bachelor_degrees.items():
        # Regex for matching both full names and abbreviations (case-insensitive)
        for abbr in abbreviations:
            # Search for the degree in the text, case-insensitive
            if re.search(r"\b" + re.escape(abbr) + r"\b", text, re.IGNORECASE):
                degrees_found.append(full_name)
                break  # Once we find the full degree name, no need to check other abbreviations for this degree

    # Return the list of degrees found
    return degrees_found


def extract_masters_degrees(text):
    # Define the full names of the degrees
    masters_degrees = {
        "Master of Technology": ["MTech", "M.Tech", "MTech.", "M.TECH", "MTech", "Master of Technology"],
        "Master of Engineering": ["ME", "M.E.", "M.E", "MEng", "M.Eng", "Master of Engineering"],
        "Master of Science": ["MSc", "M.Sc", "MSc.", "M.Sc.", "M.Sci", "M.S.", "Master of Science"],
        "Master of Arts": ["MA", "M.A.", "M.A", "MArt", "M.Ars", "Master of Arts"],
        "Master of Commerce": ["MCom", "M.Com", "MCom.", "M.Com.", "Master of Commerce"],
        "Master of Design": ["MDes", "M.Des", "Master of Design"],
        "Master of Architecture": ["m.Arch", "M.Arch", "Master of Architecture"],
        "Master of Education": ["MEd", "M.Ed", "M.Ed.", "Master of Education"],
        "Master of Fine Arts": ["MFA", "M.F.A.", "M.F.A", "Master of Fine Arts"],
        "Master of Business Administration": ["MBA", "M.B.A.", "Master of Business Administration"],
        "Master of Computer Applications": ["MCA", "M.C.A.", "Master of Computer Applications"]
    }

    # List to store the found degree names
    degrees_found = []

    # Iterate through the dictionary and check if any abbreviation or full name is found
    for full_name, abbreviations in masters_degrees.items():
        # Regex for matching both full names and abbreviations (case-insensitive)
        for abbr in abbreviations:
            # Search for the degree in the text, case-insensitive
            if re.search(r"\b" + re.escape(abbr) + r"\b", text, re.IGNORECASE):
                degrees_found.append(full_name)
                break  # Once we find the full degree name, no need to check other abbreviations for this degree

    # Return the list of degrees found
    return degrees_found


def extract_marks(text):
    # Regex patterns to match different marks formats
    marks_patterns = [
        # Matches CGPA formats (e.g., CGPA 8.5, CGPA: 9.2, CGPA=7.8)
        r"\bCGPA\s*[:=]?\s*(\d+(\.\d+)?)\b",
        r"\bC\.G\.P\.A\s*[:=]?\s*(\d+(\.\d+)?)\b",
        r"\bCGPA\s*=\s*(\d+(\.\d+)?)\b",

        # Matches percentage formats (e.g., 85%, 92.5%, 75 %)
        r"\b(\d+(\.\d+)?)\s*%?\b(?=\s*(?:percentage|percent|%))",

        # Matches aggregate format (e.g., Aggregate: 80%, Aggregate CGPA 7.9)
        r"\bAggregate\s*[:=]?\s*(\d+(\.\d+)?)\s*(%|CGPA)?\b",

        # Matches marks in general (e.g., Marks: 75/100, 90/100)
        r"\bMarks\s*[:=]?\s*(\d+(\.\d+)?)/(\d+)\b",

        # Matches GPA formats (e.g., GPA 3.5, GPA: 4.0)
        r"\bGPA\s*[:=]?\s*(\d+(\.\d+)?)\b",

        # Matches aggregate percentage (e.g., Aggregate percentage: 85%)
        r"\bAggregate\s*percentage\s*[:=]?\s*(\d+(\.\d+)?)\s*%\b",

        # Matches first-class, second-class, etc. (if present, this will be caught as a degree descriptor)
        r"\b(First|Second|Third)\s*Class\b",
    ]

    # List to store the found marks or grades
    marks_found = []

    # Iterate through each regex pattern and search for matches
    for pattern in marks_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)

        for match in matches:
            # Extract the mark or grade value from the match
            if match[0]:  # if the first group (value) is not empty
                marks_found.append(match[0])

    # Return the list of marks found
    return marks_found


def extract_12th_qualification(text):
    # Define the full names and abbreviations for 12th qualifications
    twelfth_qualifications = {
        "12th Grade": ["12th", "12th grade", "12th standard", "12th class", "12th"],
        "Higher Secondary": ["Higher Secondary", "Higher Sec.", "H.S.", "HS", "Higher Secondary School"],
        "Intermediate": ["Intermediate", "Inter", "Intermed.", "12th Intermediate", "Intermediate Class"],
        "Pre-University": ["Pre-University", "PU", "PUC", "Pre-U", "Pre-U Class"],
        "Senior Secondary": ["Senior Secondary", "Senior Sec.", "SS", "Senior Secondary School"]
    }

    # List to store the found 12th qualifications
    qualifications_found = []

    # Iterate through the dictionary and check if any abbreviation or full name is found
    for full_name, abbreviations in twelfth_qualifications.items():
        for abbr in abbreviations:
            if re.search(r"\b" + re.escape(abbr) + r"\b", text, re.IGNORECASE):
                qualifications_found.append(full_name)
                break  # Once found, no need to check other abbreviations for this qualification

    # Return the list of qualifications found
    return qualifications_found


def extract_10th_qualification(text):
    # Define the full names and abbreviations for 10th qualifications
    tenth_qualifications = {
        "10th Grade": ["10th", "10th grade", "10th standard", "10th class", "10th"],
        "Secondary School": ["Secondary School", "Sec. School", "Secondary Education", "Secondary", "SSC", "S.S.C.",
                             "S.S.C"],
        "Matriculation": ["Matriculation", "Matric", "Matric Class", "10th Matric"],
        "Senior Secondary": ["Senior Secondary", "Senior Sec.", "SS", "Senior Secondary School"]
    }

    # List to store the found 10th qualifications
    qualifications_found = []

    # Iterate through the dictionary and check if any abbreviation or full name is found
    for full_name, abbreviations in tenth_qualifications.items():
        for abbr in abbreviations:
            if re.search(r"\b" + re.escape(abbr) + r"\b", text, re.IGNORECASE):
                qualifications_found.append(full_name)
                break  # Once found, no need to check other abbreviations for this qualification

    # Return the list of qualifications found
    return qualifications_found


def extract_experience_section(resume_text: str) -> str:
    """
    Extracts the experience section from the resume text.
    """
    experience_pattern = re.compile(r"(experience)(.*?)(projects|education|skills|$)", re.DOTALL | re.IGNORECASE)
    match = experience_pattern.search(resume_text)
    if match:
        return match.group(2).strip()
    return ""


def extract_durations(resume_text: str) -> List[str]:
    """
    Extracts all duration strings from the resume text.
    """
    duration_pattern = re.compile(
        r"\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s?\d{4}\s*(?:[-–]\s*(?:present|\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s?\d{4})?)\b",
        re.IGNORECASE
    )
    durations = duration_pattern.findall(resume_text)
    return [duration.strip() for duration in durations]


def parse_date(date_str: str) -> datetime:
    """
    Parses a date string into a datetime object.
    Handles both "Month Year" and "Year" formats.
    """
    try:
        return datetime.strptime(date_str.strip(), "%B %Y")  # Try to parse as Month Year
    except ValueError:
        return datetime.strptime(date_str.strip(), "%Y")  # Fallback to Year if Month is missing


def merge_overlapping_ranges(ranges: List[Tuple[datetime, datetime]]) -> List[Tuple[datetime, datetime]]:
    """
    Merges overlapping date ranges into a single range.
    """
    if not ranges:
        return []

    # Sort ranges by start date
    sorted_ranges = sorted(ranges, key=lambda x: x[0])

    merged_ranges = []
    current_range = sorted_ranges[0]

    for next_range in sorted_ranges[1:]:
        if next_range[0] <= current_range[1]:  # Overlapping ranges
            current_range = (min(current_range[0], next_range[0]), max(current_range[1], next_range[1]))
        else:
            merged_ranges.append(current_range)
            current_range = next_range

    merged_ranges.append(current_range)
    return merged_ranges


def calculate_total_experience(durations: List[str]) -> str:
    """
    Calculates the total experience by merging overlapping ranges and summing the durations.
    """
    ranges = []

    for duration in durations:
        if '–' in duration or '-' in duration:  # Ensure we're dealing with a valid range
            start, end = re.split(r'[–-]', duration)  # Split on either en dash or hyphen

            # Parse start and end dates
            start_date = parse_date(start.strip())
            if "present" in end.strip().lower():
                end_date = datetime.now()  # Use current date for present
            else:
                end_date = parse_date(end.strip())

            ranges.append((start_date, end_date))

    # Merge overlapping ranges
    merged_ranges = merge_overlapping_ranges(ranges)

    # Calculate total months
    total_months = 0
    for start, end in merged_ranges:
        delta = (end.year - start.year) * 12 + (end.month - start.month)
        total_months += delta

    # Convert total months to years and months
    years = total_months // 12
    months = total_months % 12

    return f"{years} years and {months} months"


def get_total_experience_from_resume(resume_text: str) -> str:
    """
    Extracts the experience section, extracts durations, and calculates the total experience.
    """
    # Step 1: Extract the experience section
    experience_section = extract_experience_section(resume_text)

    if not experience_section:
        return "No experience section found."

    # Step 2: Extract durations from the experience section
    durations = extract_durations(experience_section)

    if not durations:
        return "No durations found in the experience section."

    # Step 3: Calculate the total experience
    total_experience = calculate_total_experience(durations)

    return total_experience

