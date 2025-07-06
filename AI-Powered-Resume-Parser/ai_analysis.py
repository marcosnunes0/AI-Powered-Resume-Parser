import uuid
from helper import extract_data_analysis, get_pdf_paths, read_pdf
from database import AnalyzeDatabase
from ai import GroqClient
from models.resum import Resum
from models.file import File

database = AnalyzeDatabase()
ai = GroqClient()

job = database.get_job_by_name("Senior Software Engineer Vacancy")

cv_paths = get_pdf_paths(dir="CVs")

# Process each CV individually.
for path in cv_paths:
    content = read_pdf(path)
    
    # Use the AI to generate a summary, an opinion, and a score for the CV.
    resum = ai.resum_cv(content)
    opinion = ai.generate_opinion(content, job)
    score = ai.generate_score(content, job)
    
    # Create a structured resume object with the generated data.
    resum_schema = Resum(
        id=str(uuid.uuid4()),
        job_id=job.get('id'),
        content=resum,
        file=str(path),
        opinion=opinion
    )
    
    # Create a file tracking object.
    file_schema = File(
        file_id=str(uuid.uuid4()),
        job_id=job.get('id')
    )
    
    # Extract and structure the final analysis data.
    analysis_schema = extract_data_analysis(resum, job.get('id'), resum_schema.id, score)
    
    database.resums.insert(resum_schema.model_dump())
    database.analysis.insert(analysis_schema.model_dump())
    database.files.insert(file_schema.model_dump())