import re, uuid, os, io
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

# Generate a PDF from the analysis data
def generate_analysis_pdf(candidate_name, content, opinion, score):
    doc = fitz.open()
    font_size_title = 16
    font_size_heading = 13
    font_size_body = 10
    margin = 50
    line_height = font_size_body * 1.4

    def add_page(doc):
        page = doc.new_page(width=595, height=842)  # A4
        return page, margin + 40  # return page and starting y position

    page, y = add_page(doc)
    page_width = page.rect.width
    usable_width = page_width - 2 * margin

    # Title
    page.insert_text(
        fitz.Point(margin, y),
        f"AI Analysis Report: {candidate_name}",
        fontsize=font_size_title,
        fontname="helv",
        color=(0.1, 0.1, 0.5),
    )
    y += 30

    # Score
    page.insert_text(
        fitz.Point(margin, y),
        f"Score: {score}",
        fontsize=font_size_heading,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )
    y += 25

    # Draw a separator line
    page.draw_line(
        fitz.Point(margin, y),
        fitz.Point(page_width - margin, y),
        color=(0.7, 0.7, 0.7), width=0.5
    )
    y += 15

    sections = [
        ("Resume Summary", content),
        ("AI Opinion", opinion),
    ]

    for title, text in sections:
        # Section heading
        if y > 780:
            page, y = add_page(doc)
        page.insert_text(
            fitz.Point(margin, y),
            title,
            fontsize=font_size_heading,
            fontname="helv",
            color=(0.15, 0.15, 0.4),
        )
        y += 20

        # Section body: write line by line
        clean_text = (text or '').strip()
        for line in clean_text.split('\n'):
            # Strip markdown formatting characters
            line = line.replace('**', '').replace('###', '').replace('##', '').replace('#', '').replace('*', '').strip()
            if not line:
                y += line_height * 0.5
                continue

            # Word-wrap long lines
            words = line.split()
            current_line = ''
            for word in words:
                test = f"{current_line} {word}".strip()
                text_width = fitz.get_text_length(test, fontname="helv", fontsize=font_size_body)
                if text_width > usable_width:
                    if y > 790:
                        page, y = add_page(doc)
                    page.insert_text(
                        fitz.Point(margin, y),
                        current_line,
                        fontsize=font_size_body,
                        fontname="helv",
                    )
                    y += line_height
                    current_line = word
                else:
                    current_line = test

            if current_line:
                if y > 790:
                    page, y = add_page(doc)
                page.insert_text(
                    fitz.Point(margin, y),
                    current_line,
                    fontsize=font_size_body,
                    fontname="helv",
                )
                y += line_height

        y += 10  # spacing between sections

    buffer = io.BytesIO()
    doc.save(buffer)
    doc.close()
    buffer.seek(0)
    return buffer.getvalue()