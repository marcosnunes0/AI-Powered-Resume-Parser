import re, uuid, os
import fitz
from models.analysis import Analysis

def read_pdf(file_path):
    """
    Extracts text content from a PDF file.
    """
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    
    return text

def get_pdf_paths(dir):
    """
    Retrieves the full paths of all PDF files within a specified directory.
    """
    pdf_paths = []
    
    for filename in os.listdir(dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(dir, filename)
            pdf_paths.append(file_path)
            
    return pdf_paths
    
def extract_data_analysis(resum_cv, job_id, resum_id, score):
    """
    Parsis a summarized CV, extracts key sections using regular expressions,
    and validates the data before creating an Analysis object.
    """
    sections_dict = {
        "id": str(uuid.uuid4()),
        "job_id": job_id,
        "resum_id": resum_id,
        "name": "",
        "skills": [],
        "education": [],
        "languages": [],
        "score": score
    }

    patterns = {
        "name": r"(?:## Full Name\s*|Full Name\s*|\s*Valor\s*|\s*\S*\s*|\s*)(.*)",
        "skills": r"## Skills\s*([\s\S]*?)(?=##|$)",
        "education": r"## Education\s*([\s\S]*?)(?=##|$)",
        "languages": r"## Languages\s*([\s\S]*?)(?=##|$)",
    }
    
    def clean_string(string: str) -> str:
        """Removes markdown characters and extra whitespace from a string."""
        return re.sub(r"[\*\-]+", "", string).strip()

    for section, pattern in patterns.items():
        match = re.search(pattern, resum_cv)
        if match:
            if section == "name":
                sections_dict[section] = clean_string(match.group(1))
            else:
                # Extracts and cleans list items from a matched section
                sections_dict[section] = [clean_string(item) for item in match.group(1).split('\n') if item.strip()]
                    
    # Validation to ensure that no required sections are empty
    for key in ["name", "education", 'skills']:
        if not sections_dict[key] or (isinstance(sections_dict[key], list) and not any(sections_dict[key])):
            raise ValueError(f"The section '{key}' cannot be empty or contain only empty strings.")

    return Analysis(**sections_dict)