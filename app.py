import os
import uuid
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from database import AnalyzeDatabase
from models.job import Job
from ai_analysis import run_analysis
from helper import generate_analysis_pdf

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
        ["🏠 Home", "📝 Register Job", "⚙️ Manage Jobs", "📊 Analysis"],
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
        with st.container(border=True, height=150):
            st.subheader("📝 1. Register a Job")
            st.write(
                "Define the position, main activities, prerequisites, "
                "and differentials through the form in page **Register Job**."
            )

        with st.container(border=True, height=150):
            st.subheader("🤖 3. AI Analysis")
            st.write(
                "The **Groq AI** engine summarizes, scores, and generates detailed "
                "opinions for each candidate against the job."
            )

    with col2:
        with st.container(border=True, height=150):
            st.subheader("📄 2. Upload CVs")
            st.write(
                "Place candidate PDF resumes in the CVs folder or download "
                "them directly from Google Drive."
            )

        with st.container(border=True, height=150):
            st.subheader("📊 4. View Rankings")
            st.write(
                "Explore interactive charts and tables ranking candidates "
                "so you can make informed hiring decisions."
            )

    st.divider()
    st.caption("Built with Streamlit, Groq API & Python")

# Register Job Page
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

# Manage Jobs Page
elif page == "⚙️ Manage Jobs":
    st.title("⚙️ Manage Jobs")
    st.write("Select a job vacancy to view its details, edit or delete it.")

    st.divider()

    jobs_list = database.jobs.all()

    if not jobs_list:
        st.info("📭 No job vacancies registered yet. Go to **Register Job** to create one.")
    else:
        option = st.selectbox(
            'Select a job vacancy:',
            [job.get('name') for job in jobs_list],
            index=None,
        )

        if option:
            job = database.get_job_by_name(option)

            # Edit Job
            with st.expander("✏️ Edit Job", expanded=False):
                with st.form(key="edit_job_form"):
                    new_name = st.text_input(
                        "Job Title",
                        value=job.get('name', ''),
                    )

                    new_activities = st.text_area(
                        "Main Activities",
                        value=job.get('main_activities', '').strip(),
                        height=150,
                    )

                    new_prerequisites = st.text_area(
                        "Prerequisites",
                        value=job.get('prerequisites', '').strip(),
                        height=150,
                    )

                    new_diferentials = st.text_area(
                        "Differentials",
                        value=job.get('diferentials', '').strip(),
                        height=150,
                    )

                    update_submitted = st.form_submit_button("💾 Save Changes", use_container_width=True)

                if update_submitted:
                    if not new_name.strip():
                        st.error("⚠️ The **Job Title** field is required.")
                    elif not new_activities.strip():
                        st.error("⚠️ The **Main Activities** field is required.")
                    elif not new_prerequisites.strip():
                        st.error("⚠️ The **Prerequisites** field is required.")
                    else:
                        # Check for duplicate name only if name changed
                        if new_name.strip() != job.get('name'):
                            existing = database.get_job_by_name(new_name.strip())
                            if existing:
                                st.warning("⚠️ A job vacancy with this name already exists.")
                                st.stop()

                        database.update_job_by_id(job.get('id'), {
                            'name': new_name.strip(),
                            'main_activities': new_activities.strip(),
                            'prerequisites': new_prerequisites.strip(),
                            'diferentials': new_diferentials.strip(),
                        })
                        st.success("✅ Job vacancy updated successfully.")
                        st.rerun()

            st.divider()

            # Job Details
            with st.container(border=True):
                st.subheader(f"📌 {job.get('name')}")

                st.markdown("**Main Activities:**")
                st.text(job.get('main_activities', '').strip())

                st.markdown("**Prerequisites:**")
                st.text(job.get('prerequisites', '').strip())

                st.markdown("**Differentials:**")
                st.text(job.get('diferentials', '').strip())

            # Related data counts
            analyses_count = len(database.get_analysis_by_job_id(job.get('id')))
            resums_count = len(database.get_resums_by_job_id(job.get('id')))

            if analyses_count > 0 or resums_count > 0:
                st.warning(
                    f"⚠️ This job has **{analyses_count}** analysis(es) and "
                    f"**{resums_count}** resume(s) associated. "
                    f"Deleting it will also remove all related data."
                )

            st.divider()

            # Delete with confirmation
            col1, col2 = st.columns([1, 5])
            with col1:
                delete_clicked = st.button("🗑️ Delete Job", type="primary")

            if delete_clicked:
                st.session_state["confirm_delete"] = job.get('id')

            if st.session_state.get("confirm_delete") == job.get('id'):
                st.error(f"Are you sure you want to delete **{job.get('name')}**? This action cannot be undone.")
                col_yes, col_no, _ = st.columns([1, 1, 6])
                with col_yes:
                    if st.button("✅ Yes, delete"):
                        database.delete_job_by_id(job.get('id'))
                        st.session_state.pop("confirm_delete", None)
                        st.success("✅ Job vacancy deleted successfully.")
                        st.rerun()
                with col_no:
                    if st.button("❌ Cancel"):
                        st.session_state.pop("confirm_delete", None)
                        st.rerun()
                        
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
            'Choose a vacancy:',
            [job.get('name') for job in jobs_list],
            index=None,
        )

        if option:
            job = database.get_job_by_name(option)

            # Run AI Analysis button
            if st.button('🤖 Run AI Analysis', use_container_width=False):
                try:
                    with st.spinner('Analyzing CVs with AI... This may take a few minutes.'):
                        run_analysis(job)
                    st.success('✅ AI analysis completed successfully!')
                    st.rerun()
                except FileNotFoundError:
                    st.error('⚠️ No PDF files found in the **CVs** directory. Please add CVs before running the analysis.')
                except Exception as e:
                    st.error(f'⚠️ An error occurred during analysis: {e}')

            st.divider()

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

                            col_cv, col_export = st.columns(2)

                            with col_cv:
                                try:
                                    with open(resum_data.get('file'), 'rb') as file:
                                        pdf_data = file.read()

                                        st.download_button(
                                            label=f"📄 Download {row['Name']}'s CV",
                                            data=pdf_data,
                                            file_name=f"{row['Name']}.pdf",
                                            mime='application/pdf',
                                            key=f"download_{row['ID']}",
                                            use_container_width=True,
                                        )
                                except (FileNotFoundError, TypeError):
                                    st.error(f"CV file not found for {row['Name']}.")

                            with col_export:
                                analysis_pdf = generate_analysis_pdf(
                                    candidate_name=row['Name'],
                                    content=resum_data.get('content', ''),
                                    opinion=resum_data.get('opinion', ''),
                                    score=row['Score'],
                                )
                                st.download_button(
                                    label=f"📊 Export Analysis",
                                    data=analysis_pdf,
                                    file_name=f"Analysis_{row['Name']}.pdf",
                                    mime='application/pdf',
                                    key=f"export_{row['ID']}",
                                    use_container_width=True,
                                )
                        else:
                            st.warning(f"No resum details found for {row['Name']}.")
                    st.divider()