from tinydb import TinyDB, Query

# Definition of child class "AnalyzeDatabase" inheriting from parent class "TinyDB"
class AnalyzeDatabase(TinyDB):
    # Object construction
    def __init__(self, db_path="db.json"):
        super().__init__(db_path)
        self.jobs = self.table('jobs')
        self.resums = self.table('resums')
        self.analysis = self.table('analysis')
        self.files = self.table('files')

    # Searches for a specific job by its respective name in the database
    def get_job_by_name(self, name):
        job = Query()
        result = self.jobs.search(job.name == name)
        return result[0] if result else None

    # Searches for resum summaries by resum_id
    def get_resum_by_id(self, id):
        resum = Query()
        result = self.resum.search(resum.id == id)
        return result[0] if result else None
    
    # Searches for candidate analysis based on job_id
    def get_analysis_by_job_id(self, job_id):
        analysis = Query()
        result = self.analysis.search(analysis.job_id == job_id)
        return result

    # Searches for resums summaries by job_id
    def get_resums_by_job_id(self, job_id):
        resum = Query()
        result = self.resums.search(resum.job_id == job_id)
        return result
    
    # Deletes all resums from a job_id
    def delete_all_resums_by_job_id(self, job_id):
        resum = Query()
        self.resums.remove(resum.job_id == job_id)

    # Deletes all analysis from a job_id
    def delete_all_analysis_by_job_id(self, job_id):
        analysis = Query()
        self.analysis.remove(analysis.job_id == job_id)

    # Delete all files from a job_id
    def delete_all_files_by_job_id(self, job_id):
        file = Query()
        self.files.remove(file.job_id == job_id)