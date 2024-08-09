# import streamlit as st
# import pandas as pd
# from utils import process_multiple_pdfs
# import plotly.express as px
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# from datetime import datetime
# import io

# def admin_function():
#     st.title("Admin Dashboard")

#     uploaded_files = st.file_uploader("Upload resumes (PDF, TXT)", type=['pdf', 'txt'], accept_multiple_files=True)

#     if uploaded_files:
#         processed_data = process_multiple_pdfs(uploaded_files)
#         df = pd.DataFrame(processed_data)

#         if df.empty:
#             st.warning("No data extracted from the resumes.")
#             return

#         # Handle missing data
#         df.fillna({
#             'name': 'Unknown',
#             'experience': 0,
#             'department': 'Not Specified',
#             'education': 'Not Specified',
#             'skills': 'Not Specified'
#         }, inplace=True)

#         # Sidebar Filters
#         st.sidebar.header("Filters")
        
#         # Filter by Department
#         departments = df['department'].unique().tolist()
#         selected_department = st.sidebar.multiselect("Select Department(s)", options=departments, default=departments)
#         df_filtered = df[df['department'].isin(selected_department)]

#         # Filter by Education Level
#         education_levels = df['education'].unique().tolist()
#         selected_education = st.sidebar.multiselect("Select Education Level(s)", options=education_levels, default=education_levels)
#         df_filtered = df_filtered[df_filtered['education'].isin(selected_education)]

#         # Filter by Experience Range
#         min_experience = df['experience'].min()
#         max_experience = df['experience'].max()

#         if min_experience < max_experience:
#             experience_range = st.sidebar.slider(
#                 "Select Experience Range (years)",
#                 min_value=int(min_experience),
#                 max_value=int(max_experience),
#                 value=(int(min_experience), int(max_experience)),
#                 step=1
#             )
#             df_filtered = df_filtered[
#                 (df_filtered['experience'] >= experience_range[0]) &
#                 (df_filtered['experience'] <= experience_range[1])
#             ]
#         else:
#             st.sidebar.text("Experience range not available due to lack of data.")

#         # Search and Filter by Name or Skills
#         search_term = st.sidebar.text_input("Search by Name or Skills")
#         if search_term:
#             df_filtered = df_filtered[(df_filtered['name'].str.contains(search_term, case=False)) | (df_filtered['skills'].str.contains(search_term, case=False))]

#         # Clear Filters
#         if st.sidebar.button("Clear Filters"):
#             df_filtered = df

#         # Main Content
#         st.subheader("Filtered Resume Data")
#         st.write(df_filtered)

#         # Summary Table
#         st.subheader("Summary Table")
#         summary_df = pd.DataFrame({
#             'Attribute': ['Total Resumes', 'Unique Names', 'Unique Skills', 'Unique Departments', 'Unique Education Levels'],
#             'Count': [
#                 len(df_filtered),
#                 df_filtered['name'].nunique(),
#                 df_filtered['skills'].str.split(', ').explode().nunique(),
#                 df_filtered['department'].nunique(),
#                 df_filtered['education'].nunique()
#             ]
#         })
#         st.write(summary_df)

#         # Skills Distribution
#         st.subheader("Skills Distribution")
#         all_skills = df_filtered['skills'].str.split(', ').explode()
#         skills_count = all_skills.value_counts()
#         skills_fig = px.bar(skills_count, x=skills_count.index, y=skills_count.values, labels={'x': 'Skills', 'y': 'Count'}, title='Skills Frequency')
#         st.plotly_chart(skills_fig)

#         # Department Distribution
#         st.subheader("Department Distribution")
#         department_fig = px.pie(df_filtered, names='department', title='Departments in Resumes')
#         st.plotly_chart(department_fig)

#         # Education Levels
#         st.subheader("Education Levels")
#         education_count = df_filtered['education'].value_counts()
#         education_fig = px.bar(education_count, x=education_count.index, y=education_count.values, labels={'x': 'Education Level', 'y': 'Count'}, title='Education Levels')
#         st.plotly_chart(education_fig)

#         # Experience Distribution
#         st.subheader("Experience Distribution")
#         experience_fig = px.histogram(df_filtered, x='experience', nbins=10, title='Experience Distribution')
#         st.plotly_chart(experience_fig)


      
#     else:
#         st.warning("Please upload PDF or TXT resumes to proceed with analysis.")


import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
import io
import re
from PyPDF2 import PdfReader

def extract_name(text):
    # Improved name extraction pattern
    name_pattern = r'\b(?!Python|Java|C\+\+|JavaScript|HTML|CSS|SQL|R|Go|LESS|Matlab|Git|MySQL|AWS|React|Node\.js|Spring|Express|TensorFlow|Keras|Scikit-learn|Pandas|NumPy)\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+'
    names = re.findall(name_pattern, text)
    return names[0] if names else "Unknown"

def extract_experience(text):
    # Expanded experience pattern
    experience_patterns = [
        r'(\d+)(?:\+)?\s*(?:years?|yrs?)(?:\s+of)?\s+experience',
        r'experience\s+of\s+(\d+)(?:\+)?\s*(?:years?|yrs?)',
        r'worked\s+for\s+(\d+)(?:\+)?\s*(?:years?|yrs?)'
    ]
    for pattern in experience_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return 0

def extract_education(text):
    education_patterns = {
        'PhD': r'\b(Ph\.?D\.?|Doctor of Philosophy)\b',
        'Master': r'\b(Master\'?s?|M\.?S\.?|M\.?Eng\.?|MBA)\b',
        'Bachelor': r'\b(Bachelor\'?s?|B\.?S\.?|B\.?E\.?|B\.?Tech\.?)\b'
    }
    for level, pattern in education_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            return level
    return "Unknown"

def extract_department(text):
    departments = {
        'Computer Science': r'\b(Computer Science|CS|Software Engineering)\b',
        'Information Technology': r'\b(Information Technology|IT)\b',
        'Electronics': r'\b(Electronics|ECE|Electrical Engineering)\b',
        'Mechanical': r'\b(Mechanical Engineering|Mechanical)\b'
    }
    for dept, pattern in departments.items():
        if re.search(pattern, text, re.IGNORECASE):
            return dept
    return "Computer Branches"  # Default

def process_single_pdf(file):
    if file.type == "application/pdf":
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    else:
        text = file.getvalue().decode("utf-8")
    return text

def extract_skills(text):
    skills = ['Python', 'Java', 'C++', 'JavaScript', 'HTML', 'CSS', 'SQL', 'R', 'Go', 
              'LESS', 'Matlab', 'Git', 'MySQL', 'AWS', 'React', 'Node.js', 'Spring', 
              'Express', 'TensorFlow', 'Keras', 'Scikit-learn', 'Pandas', 'NumPy']
    found_skills = [skill for skill in skills if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE)]
    return ', '.join(found_skills)

def process_multiple_pdfs(files):
    processed_data = []
    for file in files:
        content = process_single_pdf(file)
        processed_data.append({
            'name': extract_name(content),
            'skills': extract_skills(content),
            'department': extract_department(content),
            'experience': extract_experience(content),
            'education': extract_education(content)
        })
    return processed_data



def admin_function():
    st.title("Admin Dashboard")

    uploaded_files = st.file_uploader("Upload resumes (PDF, TXT)", type=['pdf', 'txt'], accept_multiple_files=True)

    if uploaded_files:
        processed_data = process_multiple_pdfs(uploaded_files)
        df = pd.DataFrame(processed_data)

        if df.empty:
            st.warning("No data extracted from the resumes.")
            return

        df.fillna({
            'name': 'Unknown',
            'experience': 0,
            'department': 'Not Specified',
            'education': 'Not Specified',
            'skills': 'Not Specified'
        }, inplace=True)

        st.sidebar.header("Filters")
        
        departments = df['department'].unique().tolist()
        selected_department = st.sidebar.multiselect("Select Department(s)", options=departments, default=departments)
        df_filtered = df[df['department'].isin(selected_department)]

        education_levels = df['education'].unique().tolist()
        selected_education = st.sidebar.multiselect("Select Education Level(s)", options=education_levels, default=education_levels)
        df_filtered = df_filtered[df_filtered['education'].isin(selected_education)]

        min_experience = df['experience'].min()
        max_experience = df['experience'].max()

        if min_experience < max_experience:
            experience_range = st.sidebar.slider(
                "Select Experience Range (years)",
                min_value=int(min_experience),
                max_value=int(max_experience),
                value=(int(min_experience), int(max_experience)),
                step=1
            )
            df_filtered = df_filtered[
                (df_filtered['experience'] >= experience_range[0]) &
                (df_filtered['experience'] <= experience_range[1])
            ]
        else:
            st.sidebar.text("Experience range not available due to lack of data.")

        search_term = st.sidebar.text_input("Search by Name or Skills")
        if search_term:
            df_filtered = df_filtered[(df_filtered['name'].str.contains(search_term, case=False)) | (df_filtered['skills'].str.contains(search_term, case=False))]

        if st.sidebar.button("Clear Filters"):
            df_filtered = df

        st.subheader("Filtered Resume Data")
        st.write(df_filtered)

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

        st.subheader("Skills Distribution")
        all_skills = df_filtered['skills'].str.split(', ').explode()
        skills_count = all_skills.value_counts()
        skills_fig = px.bar(skills_count, x=skills_count.index, y=skills_count.values, labels={'x': 'Skills', 'y': 'Count'}, title='Skills Frequency')
        st.plotly_chart(skills_fig)

        st.subheader("Department Distribution")
        department_fig = px.pie(df_filtered, names='department', title='Departments in Resumes')
        st.plotly_chart(department_fig)

        st.subheader("Education Levels")
        education_count = df_filtered['education'].value_counts()
        education_fig = px.bar(education_count, x=education_count.index, y=education_count.values, labels={'x': 'Education Level', 'y': 'Count'}, title='Education Levels')
        st.plotly_chart(education_fig)

        st.subheader("Experience Distribution")
        experience_fig = px.histogram(df_filtered, x='experience', nbins=10, title='Experience Distribution')
        st.plotly_chart(experience_fig)

    else:
        st.warning("Please upload PDF or TXT resumes to proceed with analysis.")

if __name__ == "__main__":
    admin_function()