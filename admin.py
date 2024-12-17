# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from PyPDF2 import PdfReader
# import spacy
# from spacy.matcher import Matcher
# import re

# # Load spaCy model
# nlp = spacy.load("en_core_web_sm")

# st.set_page_config(page_title="Resume Analyzer Dashboard", layout="wide")

# def extract_name(doc):
#     # Extract the first line and split it into words
#     first_line = doc.text.strip().split('\n')[0]
#     words = first_line.split()
    
#     # Check if the name is 2 to 30 characters long
#     if 2 <= len(' '.join(words)) <= 30:
#         return ' '.join(words)
    
#     # If not, use spaCy's named entity recognition as a fallback
#     for ent in doc.ents:
#         if ent.label_ == "PERSON":
#             return ent.text
    
#     return "Unknown"

# def extract_experience(doc):
#     experience_patterns = [
#         [{"LOWER": "experience"}, {"LOWER": "of"}, {"LIKE_NUM": True}, {"LOWER": {"IN": ["years", "year", "yrs", "yr"]}}],
#         [{"LIKE_NUM": True}, {"LOWER": {"IN": ["years", "year", "yrs", "yr"]}}, {"LOWER": "experience"}],
#         [{"LOWER": "worked"}, {"LOWER": "for"}, {"LIKE_NUM": True}, {"LOWER": {"IN": ["years", "year", "yrs", "yr"]}}],
#         [{"LOWER": "internship"}, {"LOWER": {"IN": ["data", "science", "visualization"]}}]
#     ]
#     matcher = Matcher(nlp.vocab)
#     for pattern in experience_patterns:
#         matcher.add("EXPERIENCE", [pattern])
#     matches = matcher(doc)
#     for _, start, end in matches:
#         span = doc[start:end]
#         for token in span:
#             if token.like_num:
#                 return float(token.text)
#     # Handle entry-level cases
#     entry_level_keywords = ['entry level', 'fresh graduate', 'recent graduate', 'internship']
#     if any(keyword in doc.text.lower() for keyword in entry_level_keywords):
#         return 0
#     return None

# def extract_education(doc):
#     education_patterns = {
#         'PhD': [{"LOWER": {"IN": ["phd", "ph.d.", "doctor", "doctorate"]}}, {"LOWER": "of", "OP": "?"}, {"LOWER": "philosophy", "OP": "?"}],
#         'Master': [{"LOWER": {"IN": ["master", "masters", "m.s.", "m.eng.", "mba"]}}],
#         'Bachelor': [{"LOWER": {"IN": ["bachelor", "bachelors", "b.s.", "b.e.", "b.tech", "btech", "bachelor of technology","b. tech"]}}]
#     }
#     matcher = Matcher(nlp.vocab)
#     for level, pattern in education_patterns.items():
#         matcher.add(level, [pattern])
#     matches = matcher(doc)
#     for match_id, start, end in matches:
#         return nlp.vocab.strings[match_id]
#     return "Unknown"

# def extract_department(doc):
#     departments = {
#         'Computer Science & Technology': ["computer science", "computer technology"],
#         'Information Technology': ["information technology"],
#         'Electronics': ["electronics", "electrical engineering", "electronic and telecommunication"],
#         'Mechanical': ["mechanical engineering"],
#         'Artificial Intelligence & Data Science': ["data science", "machine learning", "artificial intelligence", "data analysis"],
#         'Artificial Intelligence & Machine Learning': ["machine learning", "artificial intelligence"],
#         'IIOT': ["industrial internet of things"],
#         'Computer Science and Design': ["computer science and design"]
#     }
#     for dept, keywords in departments.items():
#         if any(keyword in doc.text.lower() for keyword in keywords):
#             return dept
#     return "Other"

# def extract_skills(doc):
#     skills = set(["Python", "Java", "C++", "JavaScript", "HTML", "CSS", "SQL", "React", "Angular", "Node.js",
#         "Ruby", "PHP", "Swift", "Kotlin", "C#", "R", "Go", "TypeScript", "Vue.js", "Django", "Flask",
#         "Spring", "Express.js", "Bootstrap", "Tailwind", "SASS", "LESS", "Perl", "Scala", "Rust",
#         "Matlab", "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy", "Matplotlib",
#         "Seaborn", "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Linux", "Windows Server", "Jenkins",
#         "Git", "SVN", "CI/CD", "Ansible", "Chef", "Puppet", "Terraform", "Shell Scripting",
#         "PowerShell", "Salesforce", "SAP", "Oracle", "MongoDB", "MySQL", "PostgreSQL", "Firebase",
#         "Redis", "Elasticsearch", "Kafka", "RabbitMQ", "Hadoop", "Spark", "Tableau", "Power BI",
#         "Excel", "Data Analysis", "Machine Learning", "Deep Learning", "Artificial Intelligence",
#         "Natural Language Processing", "Computer Vision", "Blockchain", "IoT", "Cybersecurity",
#         "Penetration Testing", "Network Security", "Cloud Security", "DevOps", "Agile", "Scrum",
#         "Project Management", "Leadership", "Communication", "Teamwork", "Problem Solving",
#         "Critical Thinking", "Time Management"])

#     found_skills = set()
#     for token in doc:
#         if token.text in skills:
#             found_skills.add(token.text)
#     return ', '.join(sorted(found_skills))

# def extract_cgpa(doc):
#     cgpa_pattern = r'\b(?:CGPA|GPA):\s*(\d+(?:\.\d+)?)\b'
#     match = re.search(cgpa_pattern, doc.text, re.IGNORECASE)
#     if match:
#         cgpa = float(match.group(1))
#         if 0 <= cgpa <= 10:
#             return round(cgpa, 2)
#     return None

# def extract_marks(doc):
#     marks_patterns = [
#         r'\b(?:10th|X|SSC|Matriculation)(?:\s*[:-])?\s*(\d+(?:\.\d+)?)\s*%?\b',
#         r'\b(?:12th|XII|HSC|Intermediate)(?:\s*[:-])?\s*(\d+(?:\.\d+)?)\s*%?\b'
#     ]
    
#     marks_10th = None
#     marks_12th = None
    
#     for i, pattern in enumerate(marks_patterns):
#         match = re.search(pattern, doc.text, re.IGNORECASE)
#         if match:
#             marks = float(match.group(1))
#             if 0 <= marks <= 100:
#                 if i == 0:
#                     marks_10th = marks
#                 else:
#                     marks_12th = marks
    
#     return marks_10th, marks_12th

# def process_single_pdf(file):
#     try:
#         if file.type == "application/pdf":
#             pdf_reader = PdfReader(file)
#             text = ""
#             for page in pdf_reader.pages:
#                 text += page.extract_text()
#         else:
#             text = file.getvalue().decode("utf-8")
        
#         doc = nlp(text)
        
#         name = extract_name(doc)
#         cgpa = extract_cgpa(doc)
#         marks_10th, marks_12th = extract_marks(doc)
        
#         return {
#             'name': name,
#             'skills': extract_skills(doc),
#             'department': extract_department(doc),
#             'experience': extract_experience(doc),
#             'education': extract_education(doc),
#             'cgpa': cgpa,
#             'marks_10th': marks_10th,
#             'marks_12th': marks_12th
#         }
#     except Exception as e:
#         st.error(f"Error processing file {file.name}: {str(e)}")
#         return None

# def process_multiple_pdfs(files):
#     processed_data = []
#     for file in files:
#         result = process_single_pdf(file)
#         if result:
#             processed_data.append(result)
#     return processed_data

# def admin_function():
#     st.title("Interactive Resume Analyzer Dashboard")

#     uploaded_files = st.file_uploader("Upload resumes (PDF, TXT)", type=['pdf', 'txt'], accept_multiple_files=True)

#     if uploaded_files:
#         with st.spinner('Processing resumes...'):
#             processed_data = process_multiple_pdfs(uploaded_files)
#         df = pd.DataFrame(processed_data)

#         if df.empty:
#             st.warning("No data extracted from the resumes.")
#             return

#         # Convert CGPA, 10th marks, and 12th marks to numeric, forcing errors to NaN
#         df['cgpa'] = pd.to_numeric(df['cgpa'], errors='coerce')
#         df['marks_10th'] = pd.to_numeric(df['marks_10th'], errors='coerce')
#         df['marks_12th'] = pd.to_numeric(df['marks_12th'], errors='coerce')

#         # Sidebar filters
#         st.sidebar.subheader("Filter Options")
        
#         # Show all resumes option
#         show_all = st.sidebar.checkbox("Show All Resumes", value=True)
        
#         # CGPA filter
#         if show_all:
#             cgpa_min = 0.0
#         else:
#             cgpa_min = st.sidebar.slider("Minimum CGPA", min_value=6.0, max_value=10.0, value=6.0, step=0.1)

#         # 10th Marks filter
#         if show_all:
#             marks_10th_min = 0
#         else:
#             marks_10th_min = st.sidebar.slider("Minimum 10th Marks (%)", min_value=0, max_value=100, value=60)

#         # 12th Marks filter
#         if show_all:
#             marks_12th_min = 0
#         else:
#             marks_12th_min = st.sidebar.slider("Minimum 12th Marks (%)", min_value=0, max_value=100, value=60)

#         # Skills filter
#         all_skills = set(','.join(df['skills'].dropna()).replace(', ', ',').split(','))
#         selected_skills = st.sidebar.multiselect("Select Skills", options=sorted(list(all_skills)))
        
#         # Department filter
#         departments = sorted(df['department'].unique())
#         selected_departments = st.sidebar.multiselect("Select Departments", options=departments, default=departments)
        
#         # Education filter
#         education_levels = sorted(df['education'].unique())
#         selected_education = st.sidebar.multiselect("Select Education Levels", options=education_levels, default=education_levels)

#         # Apply filters
#         mask = (df['department'].isin(selected_departments)) & \
#                (df['education'].isin(selected_education))
        
#         if not show_all:
#             mask &= (df['cgpa'].fillna(0) >= cgpa_min) & \
#                    (df['marks_10th'].fillna(0) >= marks_10th_min) & \
#                    (df['marks_12th'].fillna(0) >= marks_12th_min)
        
#         if selected_skills:
#             mask &= df['skills'].apply(lambda x: any(skill in str(x) for skill in selected_skills))

#         filtered_df = df[mask]

#         # Display filtered data
#         st.subheader(f"Filtered Resume Data ({len(filtered_df)} candidates)")
#         st.dataframe(filtered_df)

#         if not filtered_df.empty:
#             col1, col2, col3 = st.columns(3)

#             with col1:
#                 st.subheader("CGPA Distribution")
#                 valid_cgpa = filtered_df['cgpa'].dropna()
#                 if not valid_cgpa.empty:
#                     cgpa_bins = pd.cut(valid_cgpa, bins=5)
#                     cgpa_counts = cgpa_bins.value_counts().sort_index()
#                     fig_cgpa = px.pie(values=cgpa_counts.values, names=cgpa_counts.index.astype(str),
#                                       title=f'CGPA Distribution (Min: {cgpa_min})')
#                     st.plotly_chart(fig_cgpa, use_container_width=True)
#                 else:
#                     st.write("No CGPA data available")

#             with col2:
#                 st.subheader("10th Marks Distribution")
#                 valid_10th = filtered_df['marks_10th'].dropna()
#                 if not valid_10th.empty:
#                     marks_10th_bins = pd.cut(valid_10th, bins=5)
#                     marks_10th_counts = marks_10th_bins.value_counts().sort_index()
#                     fig_10th = px.pie(values=marks_10th_counts.values, names=marks_10th_counts.index.astype(str),
#                                       title=f'10th Marks Distribution (Min: {marks_10th_min}%)')
#                     st.plotly_chart(fig_10th, use_container_width=True)
#                 else:
#                     st.write("No 10th marks data available")

#             with col3:
#                 st.subheader("12th Marks Distribution")
#                 valid_12th = filtered_df['marks_12th'].dropna()
#                 if not valid_12th.empty:
#                     marks_12th_bins = pd.cut(valid_12th, bins=5)
#                     marks_12th_counts = marks_12th_bins.value_counts().sort_index()
#                     fig_12th = px.pie(values=marks_12th_counts.values, names=marks_12th_counts.index.astype(str),
#                                       title=f'12th Marks Distribution (Min: {marks_12th_min}%)')
#                     st.plotly_chart(fig_12th, use_container_width=True)
#                 else:
#                     st.write("No 12th marks data available")

#             col4, col5 = st.columns(2)

#             with col4:
#                 st.subheader("Department Distribution")
#                 fig_dept = px.pie(filtered_df, names='department', title='Departments')
#                 st.plotly_chart(fig_dept, use_container_width=True)

#             with col5:
#                 st.subheader("Education Level Distribution")
#                 fig_edu = px.pie(filtered_df, names='education', title='Education Levels')
#                 st.plotly_chart(fig_edu, use_container_width=True)

#             st.subheader("Skills Breakdown")
#             if not filtered_df['skills'].empty:
#                 skills_count = filtered_df['skills'].str.split(', ').explode().value_counts()
#                 fig_skills = px.bar(skills_count, x=skills_count.index, y=skills_count.values,
#                                     title='Top Skills',
#                                     labels={'index': 'Skills', 'value': 'Count'})
#                 fig_skills.update_layout(xaxis_tickangle=-45)
#                 st.plotly_chart(fig_skills, use_container_width=True)
                
#             st.subheader("Candidate Details")
#             for _, row in filtered_df.iterrows():
#                 with st.expander(f"{row['name']} - {row['department']}"):
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         st.write(f"**Education:** {row['education']}")
#                         st.write(f"**CGPA:** {row['cgpa']}")
#                         st.write(f"**Experience:** {row['experience']} years")
#                     with col2:
#                         st.write(f"**10th Marks:** {row['marks_10th']}%")
#                         st.write(f"**12th Marks:** {row['marks_12th']}%")
#                     st.write(f"**Skills:** {row['skills']}")

#             if st.button("Export Filtered Data to CSV"):
#                 csv = filtered_df.to_csv(index=False)
#                 st.download_button(
#                     label="Download CSV",
#                     data=csv,
#                     file_name="filtered_resume_data.csv",
#                     mime="text/csv",
#                 )
#         else:
#             st.warning("No resumes match the current filter criteria.")

#     else:
#         st.warning("Please upload PDF or TXT resumes to proceed with analysis.")

# if __name__ == "__main__":
#     admin_function()

import streamlit as st
import pandas as pd
import plotly.express as px
from PyPDF2 import PdfReader
import spacy
from spacy.matcher import Matcher
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="Resume Analyzer Dashboard", layout="wide")

def extract_name(doc):
    # Extract the first line and split it into words
    first_line = doc.text.strip().split('\n')[0]
    words = first_line.split()
    
    # Check if the name is 2 to 30 characters long
    if 2 <= len(' '.join(words)) <= 30:
        return ' '.join(words)
    
    # If not, use spaCy's named entity recognition as a fallback
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    
    return "Unknown"

def extract_experience(doc):
    experience_patterns = [
        [{"LOWER": "experience"}, {"LOWER": "of"}, {"LIKE_NUM": True}, {"LOWER": {"IN": ["years", "year", "yrs", "yr"]}}],
        [{"LIKE_NUM": True}, {"LOWER": {"IN": ["years", "year", "yrs", "yr"]}}, {"LOWER": "experience"}],
        [{"LOWER": "worked"}, {"LOWER": "for"}, {"LIKE_NUM": True}, {"LOWER": {"IN": ["years", "year", "yrs", "yr"]}}],
        [{"LOWER": "internship"}, {"LOWER": {"IN": ["data", "science", "visualization"]}}]
    ]
    matcher = Matcher(nlp.vocab)
    for pattern in experience_patterns:
        matcher.add("EXPERIENCE", [pattern])
    matches = matcher(doc)
    for _, start, end in matches:
        span = doc[start:end]
        for token in span:
            if token.like_num:
                return float(token.text)
    # Handle entry-level cases
    entry_level_keywords = ['entry level', 'fresh graduate', 'recent graduate', 'internship']
    if any(keyword in doc.text.lower() for keyword in entry_level_keywords):
        return 0
    return None

def extract_education(doc):
    education_patterns = {
        'PhD': [{"LOWER": {"IN": ["phd", "ph.d.", "doctor", "doctorate"]}}, {"LOWER": "of", "OP": "?"}, {"LOWER": "philosophy", "OP": "?"}],
        'Master': [{"LOWER": {"IN": ["master", "masters", "m.s.", "m.eng.", "mba"]}}],
        'Bachelor': [{"LOWER": {"IN": ["bachelor", "bachelors", "b.s.", "b.e.", "b.tech", "btech", "bachelor of technology","b. tech"]}}]
    }
    matcher = Matcher(nlp.vocab)
    for level, pattern in education_patterns.items():
        matcher.add(level, [pattern])
    matches = matcher(doc)
    for match_id, start, end in matches:
        return nlp.vocab.strings[match_id]
    return "Unknown"

def extract_department(doc):
    departments = {
        'Computer Science & Technology': ["computer science", "computer technology"],
        'Information Technology': ["information technology"],
        'Electronics': ["electronics", "electrical engineering", "electronic and telecommunication"],
        'Mechanical': ["mechanical engineering"],
        'Artificial Intelligence & Data Science': ["data science", "machine learning", "artificial intelligence", "data analysis"],
        'Artificial Intelligence & Machine Learning': ["machine learning", "artificial intelligence"],
        'IIOT': ["industrial internet of things"],
        'Computer Science and Design': ["computer science and design"]
    }
    for dept, keywords in departments.items():
        if any(keyword in doc.text.lower() for keyword in keywords):
            return dept
    return "Other"

def extract_skills(doc):
    skills = set(["Python", "Java", "C++", "JavaScript", "HTML", "CSS", "SQL", "React", "Angular", "Node.js",
        "Ruby", "PHP", "Swift", "Kotlin", "C#", "R", "Go", "TypeScript", "Vue.js", "Django", "Flask",
        "Spring", "Express.js", "Bootstrap", "Tailwind", "SASS", "LESS", "Perl", "Scala", "Rust",
        "Matlab", "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy", "Matplotlib",
        "Seaborn", "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Linux", "Windows Server", "Jenkins",
        "Git", "SVN", "CI/CD", "Ansible", "Chef", "Puppet", "Terraform", "Shell Scripting",
        "PowerShell", "Salesforce", "SAP", "Oracle", "MongoDB", "MySQL", "PostgreSQL", "Firebase",
        "Redis", "Elasticsearch", "Kafka", "RabbitMQ", "Hadoop", "Spark", "Tableau", "Power BI",
        "Excel", "Data Analysis", "Machine Learning", "Deep Learning", "Artificial Intelligence",
        "Natural Language Processing", "Computer Vision", "Blockchain", "IoT", "Cybersecurity",
        "Penetration Testing", "Network Security", "Cloud Security", "DevOps", "Agile", "Scrum",
        "Project Management", "Leadership", "Communication", "Teamwork", "Problem Solving",
        "Critical Thinking", "Time Management"])

    found_skills = set()
    for token in doc:
        if token.text in skills:
            found_skills.add(token.text)
    return ', '.join(sorted(found_skills))

def extract_cgpa(doc):
    cgpa_pattern = r'\b(?:CGPA|GPA|cgpa|percent):\s*(\d+(?:\.\d+)?)\b'
    match = re.search(cgpa_pattern, doc.text, re.IGNORECASE)
    if match:
        cgpa = float(match.group(1))
        if 0 <= cgpa <= 10:
            return round(cgpa, 2)
    return None

def extract_marks(text):
    # Process the text using spaCy
    doc = nlp(text)
    marks = {'ssc': None, 'hsc': None}
    current_context = None

    # Iterate over tokens and identify percentages & contexts
    for token in doc:
        token_text = token.text.lower()

        # Update context for SSC or HSC
        if token_text in ['ssc', 'class x', 'cbse']:
            current_context = 'ssc'
        elif token_text in ['hsc', 'class xii']:
            current_context = 'hsc'

        if not token.like_num:
            continue

        # Check for percentages (like '85%' or 'Percentage 85')
        if token.like_num:
            try:
                percentage = float(token.text)  # Attempt conversion
            except:
                continue
            
            # Validate percentages in correct ranges and match contexts
            next_token = token.nbor() if token.i + 1 < len(doc) else None
            if (next_token and next_token.text == '%') or (0 <= percentage <= 100):
                if current_context:
                    marks[current_context] = percentage
                    current_context = None

    return marks['ssc'], marks['hsc']
    return marks['ssc'], marks['hsc']

def process_single_pdf(file):
    try:
        if file.type == "application/pdf":
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        else:
            text = file.getvalue().decode("utf-8")
        
        doc = nlp(text)
        
        name = extract_name(doc)
        cgpa = extract_cgpa(doc)
        marks_10th, marks_12th = extract_marks(doc)
        
        return {
            'name': name,
            'skills': extract_skills(doc),
            'department': extract_department(doc),
            'experience': extract_experience(doc),
            'education': extract_education(doc),
            'cgpa': cgpa,
            'marks_10th': marks_10th,
            'marks_12th': marks_12th
        }
    except Exception as e:
        st.error(f"Error processing file {file.name}: {str(e)}")
        return None

def process_multiple_pdfs(files):
    processed_data = []
    for file in files:
        result = process_single_pdf(file)
        if result:
            processed_data.append(result)
    return processed_data

def admin_function():
    st.title("Interactive Resume Analyzer Dashboard")

    uploaded_files = st.file_uploader("Upload resumes (PDF, TXT)", type=['pdf', 'txt'], accept_multiple_files=True)

    if uploaded_files:
        with st.spinner('Processing resumes...'):
            processed_data = process_multiple_pdfs(uploaded_files)
        df = pd.DataFrame(processed_data)

        if df.empty:
            st.warning("No data extracted from the resumes.")
            return

        # Convert CGPA, 10th marks, and 12th marks to numeric, forcing errors to NaN
        df['cgpa'] = pd.to_numeric(df['cgpa'], errors='coerce')
        df['marks_10th'] = pd.to_numeric(df['marks_10th'], errors='coerce')
        df['marks_12th'] = pd.to_numeric(df['marks_12th'], errors='coerce')

        # Sidebar filters
        st.sidebar.subheader("Filter Options")
        
        # Show all resumes option
        show_all = st.sidebar.checkbox("Show All Resumes", value=True)
        
        # CGPA filter
        if show_all:
            cgpa_min = 0.0
        else:
            cgpa_min = st.sidebar.slider("Minimum CGPA", min_value=6.0, max_value=10.0, value=6.0, step=0.1)

        # 10th Marks filter
        if show_all:
            marks_10th_min = 0
        else:
            marks_10th_min = st.sidebar.slider("Minimum 10th Marks (%)", min_value=0, max_value=100, value=60)

        # 12th Marks filter
        if show_all:
            marks_12th_min = 0
        else:
            marks_12th_min = st.sidebar.slider("Minimum 12th Marks (%)", min_value=0, max_value=100, value=60)

        # Skills filter
        all_skills = set(','.join(df['skills'].dropna()).replace(', ', ',').split(','))
        selected_skills = st.sidebar.multiselect("Select Skills", options=sorted(list(all_skills)))
        
        # Department filter
        departments = sorted(df['department'].unique())
        selected_departments = st.sidebar.multiselect("Select Departments", options=departments, default=departments)
        
        # Education filter
        education_levels = sorted(df['education'].unique())
        selected_education = st.sidebar.multiselect("Select Education Levels", options=education_levels, default=education_levels)

        # Apply filters
        mask = (df['department'].isin(selected_departments)) & \
               (df['education'].isin(selected_education))
        
        if not show_all:
            mask &= (df['cgpa'].fillna(0) >= cgpa_min) & \
                   (df['marks_10th'].fillna(0) >= marks_10th_min) & \
                   (df['marks_12th'].fillna(0) >= marks_12th_min)
        
        if selected_skills:
            mask &= df['skills'].apply(lambda x: any(skill in str(x) for skill in selected_skills))

        filtered_df = df[mask]

        # Display filtered data
        st.subheader(f"Filtered Resume Data ({len(filtered_df)} candidates)")
        st.dataframe(filtered_df)

        if not filtered_df.empty:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("CGPA Distribution")
                valid_cgpa = filtered_df['cgpa'].dropna()
                if not valid_cgpa.empty:
                    cgpa_bins = pd.cut(valid_cgpa, bins=5)
                    cgpa_counts = cgpa_bins.value_counts().sort_index()
                    fig_cgpa = px.pie(values=cgpa_counts.values, names=cgpa_counts.index.astype(str),
                                      title=f'CGPA Distribution (Min: {cgpa_min})')
                    st.plotly_chart(fig_cgpa, use_container_width=True)
                else:
                    st.write("No CGPA data available")

            with col2:
                st.subheader("10th Marks Distribution")
                valid_10th = filtered_df['marks_10th'].dropna()
                if not valid_10th.empty:
                    marks_10th_bins = pd.cut(valid_10th, bins=5)
                    marks_10th_counts = marks_10th_bins.value_counts().sort_index()
                    fig_10th = px.pie(values=marks_10th_counts.values, names=marks_10th_counts.index.astype(str),
                                      title=f'10th Marks Distribution (Min: {marks_10th_min}%)')
                    st.plotly_chart(fig_10th, use_container_width=True)
                else:
                    st.write("No 10th marks data available")

            with col3:
                st.subheader("12th Marks Distribution")
                valid_12th = filtered_df['marks_12th'].dropna()
                if not valid_12th.empty:
                    marks_12th_bins = pd.cut(valid_12th, bins=5)
                    marks_12th_counts = marks_12th_bins.value_counts().sort_index()
                    fig_12th = px.pie(values=marks_12th_counts.values, names=marks_12th_counts.index.astype(str),
                                      title=f'12th Marks Distribution (Min: {marks_12th_min}%)')
                    st.plotly_chart(fig_12th, use_container_width=True)
                else:
                    st.write("No 12th marks data available")

            col4, col5 = st.columns(2)

            with col4:
                st.subheader("Department Distribution")
                fig_dept = px.pie(filtered_df, names='department', title='Departments')
                st.plotly_chart(fig_dept, use_container_width=True)

            with col5:
                st.subheader("Education Level Distribution")
                fig_edu = px.pie(filtered_df, names='education', title='Education Levels')
                st.plotly_chart(fig_edu, use_container_width=True)

            st.subheader("Skills Breakdown")
            if not filtered_df['skills'].empty:
                skills_count = filtered_df['skills'].str.split(', ').explode().value_counts()
                fig_skills = px.bar(skills_count, x=skills_count.index, y=skills_count.values,
                                    title='Top Skills',
                                    labels={'index': 'Skills', 'value': 'Count'})
                fig_skills.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_skills, use_container_width=True)
                
            st.subheader("Candidate Details")
            for _, row in filtered_df.iterrows():
                with st.expander(f"{row['name']} - {row['department']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Education:** {row['education']}")
                        st.write(f"**CGPA:** {row['cgpa']}")
                        st.write(f"**Experience:** {row['experience']} years")
                    with col2:
                        st.write(f"**10th Marks:** {row['marks_10th']}%")
                        st.write(f"**12th Marks:** {row['marks_12th']}%")
                    st.write(f"**Skills:** {row['skills']}")

            if st.button("Export Filtered Data to CSV"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="filtered_resume_data.csv",
                    mime="text/csv",
                )
        else:
            st.warning("No resumes match the current filter criteria.")

    else:
        st.warning("Please upload PDF or TXT resumes to proceed with analysis.")

if __name__ == "__main__":
    admin_function()
