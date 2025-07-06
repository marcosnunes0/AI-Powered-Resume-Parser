import os
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from database import AnalyzeDatabase

database = AnalyzeDatabase()

st.set_page_config(layout='wide', page_title='Analyzer')

# Create a dropdown menu for the user to select a job vacancy
option = st.selectbox(
    'Escolha a sua vaga:', # Label for the dropdown
    [job.get('name') for job in database.jobs.all()],
    index=None
)

data = None

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