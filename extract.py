import pdfplumber
from docx import Document

# Base class for text extraction
class TextExtractor:
    def extract_text(self, file_path):
        raise NotImplementedError("Subclasses must implement this method")

# Subclass for extracting text from DOCX files
class DocxTextExtractor(TextExtractor):
    def extract_text(self, file_path):
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip().lower()
        except Exception as e:
            print(f"Error reading DOCX file {file_path}: {e}")
            return ""

# Subclass for extracting text from PDF files
class PdfTextExtractor(TextExtractor):
    def extract_text(self, file_path):
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
            return text.strip().lower()
        except Exception as e:
            print(f"Error reading PDF file {file_path}: {e}")
            return ""

# Factory function to select the appropriate extractor based on file type
def get_text_extractor(file_path):
    if file_path.lower().endswith(".pdf"):
        return PdfTextExtractor()
    elif file_path.lower().endswith(".docx"):
        return DocxTextExtractor()
    else:
        print(f"Unsupported file format: {file_path}")
        return None

# Main function to extract text from a file
def extract_text(file_path):
    extractor = get_text_extractor(file_path)
    if extractor:
        return extractor.extract_text(file_path)
    return ""


