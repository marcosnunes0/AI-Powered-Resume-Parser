import os
import uuid
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from database import AnalyzeDatabase
from models.job import Job

database = AnalyzeDatabase()

st.set_page_config(
    layout='wide',
    page_title='Resume Analyzer',
    page_icon='🤖',
)

# Sidebar Navigation
with st.sidebar:
    st.title("🤖")
    st.caption("Resume Analyzer")
    st.divider()

    page = st.radio(
        "Menu",
        ["🏠 Home", "📝 Register Job", "📊 Analysis"],
    )

    st.divider()

    total_jobs = len(database.jobs.all())
    total_analyses = len(database.analysis.all())
    st.metric("Jobs Registered", total_jobs)
    st.metric("Analyses Performed", total_analyses)


# Home Page
if page == "🏠 Home":
    st.title("Welcome to Resume Analyzer 🤖")
    st.subheader("Analyze resumes with the power of AI")

    st.divider()

    # Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("📋 Jobs", len(database.jobs.all()))
    col2.metric("📄 Summaries", len(database.resums.all()))
    col3.metric("📊 Analyses", len(database.analysis.all()))

    st.divider()

    st.subheader("How It Works")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("📝 1. Register a Job")
            st.write(
                "Define the position, main activities, prerequisites, "
                "and differentials through the form in page **Register Job**."
            )

        with st.container(border=True):
            st.subheader("🤖 3. AI Analysis")
            st.write(
                "The **Groq AI** engine summarizes, scores, and generates detailed "
                "opinions for each candidate against the job."
            )

    with col2:
        with st.container(border=True):
            st.subheader("📄 2. Upload CVs")
            st.write(
                "Place candidate PDF resumes in the CVs folder or download "
                "them directly from Google Drive."
            )

        with st.container(border=True):
            st.subheader("📊 4. View Rankings")
            st.write(
                "Explore interactive charts and tables ranking candidates "
                "so you can make informed hiring decisions."
            )

    st.divider()
    st.caption("Built with Streamlit, Groq API & Python")

# Regiter Job Page
elif page == "📝 Register Job":
    st.title("📝 Register a New Job Vacancy")
    st.write("Fill in the details below to create a new position for candidate analysis.")

    st.divider()

    with st.form(key="job_form", clear_on_submit=True):
        name = st.text_input(
            "Job Title",
            placeholder="e.g. Senior Software Engineer Vacancy",
        )

        activities = st.text_area(
            "Main Activities",
            height=150,
            placeholder=(
                "Describe the main activities for this position...\n"
                "e.g.\n"
                "Design, develop and maintain scalable backend services and APIs\n"
                "Collaborate with cross-functional teams to define and deliver features"
            ),
        )

        prerequisites = st.text_area(
            "Prerequisites",
            height=150,
            placeholder=(
                "List the required qualifications...\n"
                "e.g.\n"
                "Bachelor's degree in Computer Science\n"
                "5+ years of professional experience in software development"
            ),
        )

        diferentials = st.text_area(
            "Differentials",
            height=150,
            placeholder=(
                "List the desired differentials...\n"
                "e.g.\n"
                "Experience with cloud platforms (AWS, Azure or GCP)\n"
                "Knowledge of containerization (Docker, Kubernetes)"
            ),
        )

        submitted = st.form_submit_button("Registar", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("⚠️ The **Job Title** field is required.")
        elif not activities.strip():
            st.error("⚠️ The **Main Activities** field is required.")
        elif not prerequisites.strip():
            st.error("⚠️ The **Prerequisites** field is required.")
        else:
            existing = database.get_job_by_name(name.strip())
            if existing:
                st.warning("⚠️ A job vacancy with this name already exists.")
            else:
                job = Job(
                    id=str(uuid.uuid4()),
                    name=name.strip(),
                    main_activities=activities.strip(),
                    prerequisites=prerequisites.strip(),
                    diferentials=diferentials.strip(),
                )
                database.jobs.insert(job.model_dump())
                st.success("✅ Job vacancy successfully registered.")
                st.balloons()

# Analysis Page
elif page == "📊 Analysis":
    st.title("📊 Candidate Analysis")
    st.write("Select a job vacancy to view the ranking and detailed candidate reviews.")

    st.divider()

    jobs_list = database.jobs.all()

    if not jobs_list:
        st.info("📭 No job vacancies registered yet. Go to **Register Job** to create one.")
    else:
        option = st.selectbox(
            'Escolha uma vaga:',
            [job.get('name') for job in jobs_list],
            index=None,
        )

        if option:
            job = database.get_job_by_name(option)
            data = database.get_analysis_by_job_id(job.get('id'))

            df = pd.DataFrame(
                data if data else [],
                columns=[
                    'name',
                    'education',
                    'skills',
                    'language',
                    'score',
                    'resum_id',
                    'id'
                ]
            )

            df.rename(
                columns={
                    'name': 'Name',
                    'education': 'Education',
                    'skills': 'Skills',
                    'language': 'Language',
                    'score': 'Score',
                    'resum_id': 'Resum_id',
                    'id': 'ID'
                },
                inplace=True
            )

            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_pagination(paginationAutoPageSize=True)

            if data:
                gb.configure_column('Score', header_name='Score', sort='desc') # Sort score descending
                gb.configure_selection(selection_mode='multiple', use_checkbox=True)

            grid_options = gb.build()

            st.subheader('Candidate Ranking')
            st.bar_chart(df, x='Name', y='Score', color='Name', horizontal=True)

            response = AgGrid(
                df,
                gridOptions=grid_options,
                enable_enterprise_modules=True,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                theme='streamlit'
            )

            selected_candidates = response.get('selected_rows', [])
            candidates_df = pd.DataFrame(selected_candidates)

            resums = database.get_resums_by_job_id(job.get('id'))

            # Function to delete resume files from the filesystem
            def delete_files_resum(resums):
                for resum in resums:
                    path = resum.get('file')
                    if os.path.isfile(path):
                        os.remove(path)

            if st.button('Clear Analysis'):
                database.delete_all_resums_by_job_id(job.get('id'))
                database.delete_all_analysis_by_job_id(job.get('id'))
                database.delete_all_files_by_job_id(job.get('id'))

            if not candidates_df.empty:
                for idx, row in candidates_df.iterrows():
                    with st.container():
                        st.subheader(f"Analysis for: {row['Name']}")
                        if resum_data := database.get_resum_by_id(row['Resum_id']):
                            st.markdown("### Resume Content")
                            st.markdown(resum_data.get('content'))
                            st.markdown("### Opinion")
                            st.markdown(resum_data.get('opinion'))

                            try:
                                with open(resum_data.get('file'), 'rb') as file:
                                    pdf_data = file.read()

                                    st.download_button(
                                        label=f"Download CV {row['Name']}",
                                        data=pdf_data,
                                        file_name=f"{row['Name']}.pdf",
                                        mime='application/pdf',
                                        key=f"download_{row['ID']}"
                                    )
                            except (FileNotFoundError, TypeError):
                                st.error(f"CV file not found for {row['Name']}.")
                        else:
                            st.warning(f"No resum details found for {row['Name']}.")
                    st.divider()