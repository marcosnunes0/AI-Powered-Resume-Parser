import uuid
from models.job import Job
from database import AnalyzeDatabase

database = AnalyzeDatabase()

name = "Senior Software Engineer Vacancy"

activities = '''
Design, develop and maintain scalable backend services and APIs
Collaborate with cross-functional teams (product, UX/UI, QA) to define and deliver features
Perform code reviews, ensure code quality and best practices
Troubleshoot, debug and optimize application performance
Mentor junior engineers and contribute to a culture of continuous improvement
'''

prerequisites = '''
Bachelor’s or Master’s degree in Computer Science, Engineering or related field
5+ years of professional experience in software development
Proficiency in at least one modern backend language (e.g. Java, C#, Python, Go)
Solid understanding of RESTful API design and microservices architecture
Experience with relational and NoSQL databases (e.g. PostgreSQL, MongoDB)
Familiarity with version control (Git) and CI/CD pipelines
Strong problem-solving skills and ability to work in agile environments
Excellent communication skills in English
'''

diferentials = '''
Hands-on experience with cloud platforms (AWS, Azure or GCP)
Knowledge of containerization and orchestration (Docker, Kubernetes)
Background in Event-Driven Architecture and message brokers (Kafka, RabbitMQ)
Experience with infrastructure-as-code tools (Terraform, CloudFormation)
Contributions to open-source projects or active technical blog presence
Certifications in cloud or security domains (e.g. AWS Certified, CISSP)
'''

job = Job(
    id=str(uuid.uuid4()),
    name=name,
    main_activities=activities,
    prerequisites=prerequisites,
    diferentials=diferentials
)

database.jobs.insert(job.model_dump())