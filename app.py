import streamlit as st
from pytrials.client import ClinicalTrials
import pandas as pd

ct = ClinicalTrials()

available_fields = [
    "NCT Number", "Study Title", "Study URL", "Acronym", "Study Status", "Brief Summary", "Study Results",
    "Conditions", "Interventions", "Primary Outcome Measures", "Secondary Outcome Measures", "Other Outcome Measures",
    "Sponsor", "Collaborators", "Sex", "Age", "Phases", "Enrollment", "Funder Type", "Study Type", "Study Design",
    "Other IDs", "Start Date", "Primary Completion Date", "Completion Date", "First Posted", "Results First Posted",
    "Last Update Posted", "Locations", "Study Documents"
]

st.title('Clinical Trials Search')

disease_type = st.text_input('Enter the disease type (for multiple diseases add a +):', 'Coronavirus+COVID')

selected_fields = st.multiselect('Select the fields you want to include:', available_fields, default=["NCT Number", "Study Title", "Conditions"])

max_studies = st.number_input('Maximum number of studies to retrieve:', min_value=1, max_value=1000, value=100)

if st.button('Search'):
    with st.spinner('Fetching data...'):
        try:
            study_fields = ct.get_study_fields(search_expr=disease_type, fields=selected_fields, max_studies=max_studies)

            df_study_fields = pd.DataFrame(study_fields)

            st.dataframe(df_study_fields)

            csv = df_study_fields.to_csv(index=False)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name="study_fields.csv",
                mime="text/csv",
            )

            st.write(f"Number of rows: {df_study_fields.shape[0]}")
            st.write(f"Number of columns: {df_study_fields.shape[1]}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

st.success('Done!')
