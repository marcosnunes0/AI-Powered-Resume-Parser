import re
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    def __init__(self, model_id="llama-3.3-70b-versatile"):
        self.model_id = model_id
        self.client = ChatGroq(model=self.model_id)
    
    def generate_response(self, prompt):
        response = self.client.invoke(prompt)
        return response.content
    
    def resum_cv(self, cv):
        """
        Summarizes a CV by extracting key information and formatting it in Markdown.
        """
        prompt = f'''
        Resum CV Request in Markdown:

        Candidate resum to summarize:

        {cv}

        Please generate a summary of the provided resum, formatted in Markdown, strictly following the template below.
        Do not add extra sections, tables or any other type of formatting other than that specified.
        Fill out each section with the relevant information, ensuring that the summary is accurate and focused.

        **Expected Output Format:**

        ```markdown
        ## Full Name
        full_name here

        ## Experience
        experience here

        ## Skills
        skills here

        ## Education
        education here

        ## Languages
        languages ​​here
        '''
        
        result_raw = self.generate_response(prompt)
        
        try:
            result = result_raw.split('```markdown')[1]
        except: 
            result = result_raw
        
        return result
    
    def generate_score(self, cv, job, max_attempts=10):
        """
        Evaluates a CV against a job description and generates a score from 0 to 10.
        It considers experience, technical skills, education, languages, strengths, and weaknesses.
        """
        prompt = f'''
        Objective: To evaluate a cv based on a specific job opening and calculate the final score. The maximum score is 10.0.

        Instructions:

        1. Experience (Weight: 30%) **: Evaluate the relevance of the experience in relation to the job opening.
        2. Technical Skills (Weight: 25%) **: Check the alignment of technical skills with the job requirements.
        3. Education (Weight: 10%) **: Evaluate the relevance of the academic background to the job opening.
        4. Languages ​​(Weight: 10%) **: Evaluate the languages ​​and their proficiency in relation to the job opening.
        5. Strengths (Weight: 15%) **: Evaluate the relevance of the strengths to the job opening.
        6. Weaknesses (Discount of up to 10%) **: Evaluate the severity of the weaknesses in relation to the job opening.

        Candidate's CV

        {cv}

        Position the candidate is applying for

        {job}

        Expected Output:
        ```
        Final Score: x.x
        ```

        Attention: Be strict when assigning grades. The maximum grade is 10.0, and the output should only contain "Final Score: x.x".
        '''
        
        for attempt in range(max_attempts):
            result_raw = self.generate_response(prompt)
            score = self.extract_score_from_result(result_raw)
            
            if score is not None:
                return score
    
    def extract_score_from_result(self, result_raw):
        """
        Extracts the score from the raw text using a regular expression.
        The regex looks for "Final Score" and captures the following number.
        """
        pattern = r"(?i)Final Score[:\s]*([\d,.]+(?:/\d{1,2})?)"
        
        match = re.search(pattern, result_raw)
        if match:
            score_str = match.group(1)
            if '/' in score_str:
                score_str = score_str.split('/')[0]
            
            return float(score_str.replace(',', '.'))
        return None
    
    def generate_opnion(self, cv, job):
        """
        Generates a critical and detailed review of a CV in relation to a job description.
        The review includes points of alignment, misalignment, and attention.
        """
        prompt = f'''
        Please review the cv provided against the job description and create a highly critical and detailed review. Your review should include the following points:

        You should think like the head recruiter who is reviewing and generating a descriptive review of the candidate’s resume who applied for the position.

        Format your response professionally, using large headings in sections.

        1. **Points of Alignment**: Identify and discuss the aspects of the resume that are directly aligned with the job requirements. Include specific examples of experiences, skills, or qualifications that match what the position is looking for.

        2. **Points of Misalignment**: Highlight and discuss areas where the candidate does not meet the job requirements. This may include a lack of experience in key areas, a lack of specific technical skills, or qualifications that do not match the expectations of the position.

        3. **Points of Attention**: Identify and discuss features of the resume that deserve special attention. This may include aspects such as how often the candidate changes jobs, gaps in their work history, or personal characteristics that may influence job performance, either positively or negatively.

        Your analysis should be objective, based on evidence presented in the resume and job description. Be detailed and provide an honest assessment of the candidate's strengths and weaknesses in relation to the position.

        **Original cv:**
        {cv}

        **Job Description:**
        {job}

        You should return this critical analysis formatted as if it were an analytical report of the resume with the position, it should be formatted with large, bold headings.
        '''
        response = self.generate_response(prompt)
        
        return response