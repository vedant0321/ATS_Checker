import streamlit as st
import pandas as pd
from utils import process_multiple_pdfs
import os
from datetime import datetime
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt


st.set_page_config(initial_sidebar_state="collapsed")
def admin_function():
    st.title("Admin Dashboard")

    uploaded_files = st.file_uploader("Upload resumes (PDF, TXT)", type=['pdf', 'txt'], accept_multiple_files=True)

    if uploaded_files:
        processed_data = process_multiple_pdfs(uploaded_files)
        df = pd.DataFrame(processed_data)

        if df.empty:
            st.warning("No data extracted from the resumes.")
            return

        # Sidebar Filters
        st.sidebar.header("Filters")
        
        # Filter by Department
        departments = df['department'].unique().tolist()
        selected_department = st.sidebar.multiselect("Select Department(s)", options=departments, default=departments)
        df_filtered = df[df['department'].isin(selected_department)]

        # Filter by Education Level
        education_levels = df['education'].unique().tolist()
        selected_education = st.sidebar.multiselect("Select Education Level(s)", options=education_levels, default=education_levels)
        df_filtered = df_filtered[df_filtered['education'].isin(selected_education)]

        # Filter by Experience Range
        min_experience = df['experience'].min()
        max_experience = df['experience'].max()

        if min_experience < max_experience:
            experience_range = st.sidebar.slider(
                "Select Experience Range (years)",
                min_value=min_experience,
                max_value=max_experience,
                value=(min_experience, max_experience),
                step=1
            )
            df_filtered = df_filtered[
                (df_filtered['experience'] >= experience_range[0]) &
                (df_filtered['experience'] <= experience_range[1])
            ]
        else:
            st.sidebar.text("Experience range not available due to lack of data.")

        # Search and Filter by Name or Skills
        search_term = st.sidebar.text_input("Search by Name or Skills")
        if search_term:
            df_filtered = df_filtered[(df_filtered['name'].str.contains(search_term, case=False)) | (df_filtered['skills'].str.contains(search_term, case=False))]

        # Clear Filters
        if st.sidebar.button("Clear Filters"):
            df_filtered = df

        # Main Content
        st.subheader("Filtered Resume Data")
        st.write(df_filtered)

        # Summary Table
        st.subheader("Summary Table")
        summary_df = pd.DataFrame({
            'Attribute': ['Total Resumes', 'Unique Names', 'Unique Skills', 'Unique Departments', 'Unique Education Levels'],
            'Count': [
                len(df_filtered),
                df_filtered['name'].nunique(),
                df_filtered['skills'].str.split(', ').explode().nunique(),
                df_filtered['department'].nunique(),
                df_filtered['education'].nunique()
            ]
        })
        st.write(summary_df)

        # Skills Distribution
        st.subheader("Skills Distribution")
        all_skills = df_filtered['skills'].str.split(', ').sum()
        skills_count = pd.Series(all_skills).value_counts()
        skills_fig = px.bar(skills_count, x=skills_count.index, y=skills_count.values, labels={'x': 'Skills', 'y': 'Count'}, title='Skills Frequency')
        st.plotly_chart(skills_fig)

        # Department Distribution
        st.subheader("Department Distribution")
        department_fig = px.pie(df_filtered, names='department', title='Departments in Resumes')
        st.plotly_chart(department_fig)

        # Education Levels
        st.subheader("Education Levels")
        education_count = df_filtered['education'].value_counts()
        education_fig = px.bar(education_count, x=education_count.index, y=education_count.values, labels={'x': 'Education Level', 'y': 'Count'}, title='Education Levels')
        st.plotly_chart(education_fig)

        # Experience Distribution
        st.subheader("Experience Distribution")
        experience_fig = px.histogram(df_filtered, x='experience', nbins=10, title='Experience Distribution')
        st.plotly_chart(experience_fig)

        # Skills Word Cloud
        st.subheader("Skills Word Cloud")
        all_skills_text = ' '.join(all_skills)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_skills_text)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        # Export Options
        st.subheader("Export Options")
        export_format = st.selectbox("Select Export Format", ['CSV', 'Excel', 'PDF'])
        if st.button("Export Data"):
            if export_format == 'CSV':
                csv_data = df_filtered.to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv_data,
                    file_name=f"resume_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            elif export_format == 'Excel':
                excel_data = pd.DataFrame.to_excel(df_filtered, index=False)
                st.download_button(
                    label="Download as Excel",
                    data=excel_data,
                    file_name=f"resume_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.ms-excel"
                )
            elif export_format == 'PDF':
                pdf_data = df_filtered.to_pdf(index=False)
                st.download_button(
                    label="Download as PDF",
                    data=pdf_data,
                    file_name=f"resume_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )

    else:
        st.warning("Please upload PDF or TXT resumes to proceed with analysis.")