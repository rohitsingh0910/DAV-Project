import re

# Base class for text extraction
class TextExtractor:
    def extract(self, text):
        raise NotImplementedError("Subclasses must implement this method")

# Subclass for extracting skills
class SkillsExtractor(TextExtractor):
    def extract(self, text):
        skills_pattern = r"\b(python|linux|microcontrollers|c++|embedded c|c|Communication Protocol|java|c\+\+|data science|machine learning|sql|r|excel|spring|html|css|javascript|go|ruby|GPIO|I2C|SPI|UART|CAN|ARM cortex|AVR|PIC|RTOS|FreeRTOS|C/C++|I2C/SPI/UART|GDB|OpenOCD|JTAG debuggers|TCP/IP|UDP|MQTT|HTTP)\b"
        skills = re.findall(skills_pattern, text, re.IGNORECASE)
        # Clean up skills by removing duplicates and irrelevant words
        skills = list(set([skill.lower() for skill in skills if skill.lower() not in ['r', 'following']]))
        skills.sort()
        return skills

# Subclass for extracting role
class RoleExtractor(TextExtractor):
    def extract(self, text):
        role_pattern = r"(role|position|title|Job Role):?\s*([A-Za-z\s]+)(?=\s*at|\s*$)"
        roles = re.findall(role_pattern, text, re.IGNORECASE)
        return roles[0][1] if roles else "Not found"

# Subclass for extracting experience years
class ExperienceExtractor(TextExtractor):
    def extract(self, text):
        years_pattern = r"\b(\d+\s*(?:\+|to|-)?\s*\d*)\s*(?:years?|yrs?)\b"
        experience_years = re.findall(years_pattern, text, re.IGNORECASE)
        return experience_years[0] if experience_years else "Not found"

# Subclass for extracting qualification
class QualificationExtractor(TextExtractor):
    def extract(self, text):
        qualification_pattern = r"\b(?:Undergraduate|Graduate|Post[-\s]?Graduate|Postgraduate|B(?:\.?Tech|\.?E|achelors?)|M(?:\.?Tech|\.?E|asters?)|B\.?Sc|M\.?Sc|B\.?A|M\.?A|Ph\.?D|Diploma|Associate\sDegree)\b"
        qualifications = list(set(re.findall(qualification_pattern, text, re.IGNORECASE)))
        return qualifications

# Main class for extracting all details
class ResumeExtractor:
    def __init__(self):
        self.skill_extractor = SkillsExtractor()
        self.role_extractor = RoleExtractor()
        self.experience_extractor = ExperienceExtractor()
        self.qualification_extractor = QualificationExtractor()

    def extract_details(self, text):
        skills = self.skill_extractor.extract(text)
        role = self.role_extractor.extract(text)
        years_of_experience = self.experience_extractor.extract(text)
        qualification = self.qualification_extractor.extract(text)
        return skills, role, years_of_experience, qualification

# Example usage
def extract_skills_role_experience_qualification(text):
    extractor = ResumeExtractor()
    skills, role, years_of_experience, qualification = extractor.extract_details(text)
    return skills, role, years_of_experience, qualification


