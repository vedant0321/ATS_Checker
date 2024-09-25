import streamlit as st
import pandas as pd
import plotly.express as px
import re
from PyPDF2 import PdfReader

def extract_name(text):
    lines = text.split('\n')
    
    for line in lines[:5]:  
        line = re.sub(r'[^a-zA-Z\s]', '', line).strip()
        words = line.split()
        if len(words) >= 2:
            return ' '.join(words[:2])
        elif len(words) == 1 and len(words[0]) >= 2:
            return words[0]
    
    return "Unknown"

def extract_experience(text):
    experience_patterns = [
        r'(\d+(?:\.\d+)?)(?:\+)?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)',
        r'experience\s+of\s+(\d+(?:\.\d+)?)(?:\+)?\s*(?:years?|yrs?)',
        r'worked\s+for\s+(\d+(?:\.\d+)?)(?:\+)?\s*(?:years?|yrs?)'
    ]
    for pattern in experience_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    entry_level_keywords = ['entry level', 'fresh graduate', 'recent graduate', 'internship']
    if any(keyword in text.lower() for keyword in entry_level_keywords):
        return 0
    return None  # Return None instead of 0 if no experience found

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
        'Computer Science & Technology': r'\b(Computer Science|C.Tech|CT)\b',
        'Information Technology': r'\b(Information Technology|IT)\b',
        'Electronics': r'\b(Electronics|ECE|Electrical Engineering|Eletronic and telecommunication)\b',
        'Mechanical': r'\b(Mechanical Engineering|Mechanical)\b',
        'Artificial Intelligence & Data Science': r'\b(Data Science|Machine Learning|AI|Artificial Intelligence|Data Analysis|AI&DS|AIDS)\b',
        'Artificial Intelligence & Machine Learning':r'\b(Machine Learning|AI|Artificial Intelligence|ML)\b',
        'IIOT': r'\b(IIOT|Industrial Internet of Things)\b',
        'Computer Science and Design': r'\b(CSD|computer science and design)\b',
    }
    for dept, pattern in departments.items():
        if re.search(pattern, text, re.IGNORECASE):
            return dept
    return "Other"

def extract_skills(text):
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
    for skill in skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.add(skill)
    return ', '.join(sorted(found_skills))

def extract_cgpa(text):
    cgpa_pattern = r'(?:CGPA|GPA)[:]\s*(\d+(?:\.\d+)?)'
    match = re.search(cgpa_pattern, text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None

def extract_marks(text):
    # Regex pattern for 10th marks
    marks_pattern_10th = r'(?:10th|X|Class X|CBSE).*?Percentage:\s*(\d{1,3}(?:\.\d+)?)\s*%'
    # Regex pattern for 12th marks
    marks_pattern_12th = r'(?:12th|XII|HSC).*?Percentage:\s*(\d{1,3}(?:\.\d+)?)\s*%'
    
    match_10th = re.search(marks_pattern_10th, text, re.IGNORECASE)
    marks_10th = float(match_10th.group(1)) if match_10th else None
    
    match_12th = re.search(marks_pattern_12th, text, re.IGNORECASE)
    marks_12th = float(match_12th.group(1)) if match_12th else None
    
    return marks_10th, marks_12th

def process_single_pdf(file):
    try:
        if file.type == "application/pdf":
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        else:
            text = file.getvalue().decode("utf-8")
        return text
    except Exception as e:
        st.error(f"Error processing file {file.name}: {str(e)}")
        return None

def process_multiple_pdfs(files):
    processed_data = []
    for file in files:
        content = process_single_pdf(file)
        if content:
            marks_10th, marks_12th = extract_marks(content)
            processed_data.append({
                'name': extract_name(content),
                'skills': extract_skills(content),
                'department': extract_department(content),
                'experience': extract_experience(content),
                'education': extract_education(content),
                'cgpa': extract_cgpa(content),
                'marks_10th': marks_10th,
                'marks_12th': marks_12th
            })
    return processed_data

# Main Streamlit app
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

        # Sidebar filters
        st.sidebar.title("Filters and Visualizations")
        st.sidebar.header("Filters")
        
        # CGPA filter
        cgpa_min, cgpa_max = st.sidebar.slider("CGPA Range", 0.0, 10.0, (0.0, 10.0), 0.1)
        
        # 10th Marks filter
        marks_10th_min, marks_10th_max = st.sidebar.slider("10th Marks Range (%)", 0, 100, (0, 100), 1)
        
        # 12th Marks filter
        marks_12th_min, marks_12th_max = st.sidebar.slider("12th Marks Range (%)", 0, 100, (0, 100), 1)

        # Skills filter
        all_skills = set(','.join(df['skills'].dropna()).replace(', ', ',').split(','))
        selected_skills = st.sidebar.multiselect("Select Skills", options=list(all_skills))
        
        # Department filter
        departments = df['department'].unique()
        selected_departments = st.sidebar.multiselect("Select Departments", options=departments, default=departments)
        
        # Education filter
        education_levels = df['education'].unique()
        selected_education = st.sidebar.multiselect("Select Education Levels", options=education_levels, default=education_levels)

        # Apply filters
        mask = (df['cgpa'].between(cgpa_min, cgpa_max, inclusive='both')) & \
               (df['marks_10th'].between(marks_10th_min, marks_10th_max, inclusive='both')) & \
               (df['marks_12th'].between(marks_12th_min, marks_12th_max, inclusive='both')) & \
               (df['department'].isin(selected_departments)) & \
               (df['education'].isin(selected_education))
        
        if selected_skills:
            mask &= df['skills'].apply(lambda x: any(skill in str(x) for skill in selected_skills))

        filtered_df = df[mask]

        # Display filtered data
        st.subheader("Filtered Resume Data")
        st.dataframe(filtered_df)

        if not filtered_df.empty:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("CGPA Distribution")
                cgpa_bins = pd.cut(filtered_df['cgpa'].dropna(), bins=5)
                cgpa_counts = cgpa_bins.value_counts().sort_index()
                fig_cgpa = px.pie(values=cgpa_counts.values, names=cgpa_counts.index.astype(str),
                                  title='CGPA Distribution')
                st.plotly_chart(fig_cgpa, use_container_width=True)

            with col2:
                st.subheader("10th Marks Distribution")
                marks_10th_bins = pd.cut(filtered_df['marks_10th'].dropna(), bins=5)
                marks_10th_counts = marks_10th_bins.value_counts().sort_index()
                fig_10th = px.pie(values=marks_10th_counts.values, names=marks_10th_counts.index.astype(str),
                                  title='10th Marks Distribution')
                st.plotly_chart(fig_10th, use_container_width=True)

            with col3:
                st.subheader("12th Marks Distribution")
                marks_12th_bins = pd.cut(filtered_df['marks_12th'].dropna(), bins=5)
                marks_12th_counts = marks_12th_bins.value_counts().sort_index()
                fig_12th = px.pie(values=marks_12th_counts.values, names=marks_12th_counts.index.astype(str),
                                  title='12th Marks Distribution')
                st.plotly_chart(fig_12th, use_container_width=True)

            st.subheader("Department Distribution")
            fig_dept = px.pie(filtered_df, names='department', title='Departments')
            st.plotly_chart(fig_dept, use_container_width=True)

            st.subheader("Skills Breakdown")
            skills_count = filtered_df['skills'].str.split(', ').explode().value_counts()
            fig_skills = px.bar(skills_count, x=skills_count.index, y=skills_count.values,
                                title='Top Skills',
                                labels={'index': 'Skills', 'value': 'Count'})
            st.plotly_chart(fig_skills, use_container_width=True)

            st.subheader("Candidate Details")
            for _, row in filtered_df.iterrows():
                with st.expander(f"{row['name']} - {row['department']}"):
                    st.write(f"CGPA: {row['cgpa']}")
                    st.write(f"10th Marks: {row['marks_10th']}%")
                    st.write(f"12th Marks: {row['marks_12th']}%")
                    st.write(f"Education: {row['education']}")
                    st.write(f"Experience: {row['experience']} years")
                    st.write(f"Skills: {row['skills']}")

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