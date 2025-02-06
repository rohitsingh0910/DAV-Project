class Skill:
    """For Calculating the skill score of each resume according to mathched skills with
    the job description"""
    def __init__(self, skills, job_skills):
        """skills and job skills used to compare the data"""
        self.skills = skills
        self.job_skills = job_skills

    def skill_score(self):
        """Firstly convert each skill to lower characters and then mathched
        according to how many skills mathched with job description : (skill_mathched/length of job description skill)*100"""
        candidate_skills_normalized = {skill.lower() for skill in self.skills}
        job_skills_normalized = {skill.lower() for skill in self.job_skills}
        # Find the intersection of both sets to get the matching skills
        matching_skills = candidate_skills_normalized & job_skills_normalized
        # Count the matching skills
        skill_matching_count = len(matching_skills)
        # skill_score
        skill_score = (skill_matching_count / len(self.job_skills)) * 100
        return skill_score

class Experience:
    """For calculating the experience and match with the job description if resume experience is
    in the range of job description then experience_score is 100, else the experience is non-zero then 20, and
    if the experience is between 0.5 to min job-experience then experience score is 50"""

    def __init__(self, job_experience, year):
        self.job_experience = job_experience
        self.year = year

    def experience_score(self):
        try:
            experience = float(self.year.split()[0])  # Extract the number of years from the "X years" format
        except ValueError:
            experience = 0  # If experience format is unexpected, default to 0

        experience_matching_count = 0
        # Handling case for "to" range in job_experience
        if 'to' in self.job_experience:
            experience_range = self.job_experience.split('to')
            start = float(experience_range[0].strip())
            end = float(experience_range[1].strip())
            if start <= experience <= end:
                experience_matching_count = 1
            elif 0.5 <= experience < start:
                experience_matching_count = 0.5
            elif experience < 0.5:
                experience_matching_count = 0.2
            else:
                experience_matching_count = 0
        elif 'to' not in self.job_experience:
            experience_range = float(self.job_experience)
            if experience_range <= experience:
                experience_matching_count = 1
            else:
                experience_matching_count = 0

        experience_score = experience_matching_count * 100
        return experience_score


class Qualification:
    def __init__(self, bachelor_degree, masters_degree, marks, job_qualification):
        self.bachelor_degree = bachelor_degree
        self.masters_degree = masters_degree
        self.marks = marks
        self.job_qualification = job_qualification

    def check_qualification(self, degree, job_qualification):
        # Convert qualifications to lowercase for case-insensitive comparison
        candidate_qualifications_normalized = [qualification.lower() for qualification in degree]
        required_qualifications_normalized = [qualification.lower() for qualification in job_qualification]

        matching_qualifications = [qualification for qualification in candidate_qualifications_normalized if
                                   any(req in qualification for req in required_qualifications_normalized)]
        return matching_qualifications

    def marks_converter(self, marks_10th, marks_12th, cgpa):
        # Convert the marks to a consistent scale
        if 0 <= marks_10th <= 10:
            marks_10th = round(marks_10th * 9.5)
        if 0 <= marks_12th <= 10:
            marks_12th = round(marks_12th * 9.5)
        if 0 <= cgpa <= 10:
            cgpa = round(cgpa * 9.5)
        return marks_10th, marks_12th, cgpa

    def check_qualification_criteria(self, marks_10th, marks_12th, cgpa):
        qualification_matching_count = 0
        marks_10th, marks_12th, cgpa = self.marks_converter(marks_10th, marks_12th, cgpa)
        if marks_10th >= 75.00 and marks_12th >= 65.00 and cgpa >= 65.00:
            qualification_matching_count = 1
        else:
            qualification_matching_count = 0
        return qualification_matching_count

    def qualification_score(self):
        degree = self.bachelor_degree or self.masters_degree
        qualification_matching = self.check_qualification(degree, self.job_qualification)
        if qualification_matching:
            qualification_check = self.check_qualification_criteria(
                float(self.marks[2]), float(self.marks[1]), float(self.marks[0])
            )
            qualification_score = qualification_check * 100
        else:
            qualification_score = 0
        return qualification_score
