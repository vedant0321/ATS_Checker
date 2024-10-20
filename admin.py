import streamlit as st
import pandas as pd
import plotly.express as px
import re
from PyPDF2 import PdfReader

st.set_page_config(page_title="Resume Analyzer Dashboard", layout="wide")

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
    return None

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
        'Computer Science & Technology': r'\b(Computer Science|C\.Tech|CT)\b',
        'Information Technology': r'\b(Information Technology|IT)\b',
        'Electronics': r'\b(Electronics|ECE|Electrical Engineering|Electronic and telecommunication)\b',
        'Mechanical': r'\b(Mechanical Engineering|Mechanical)\b',
        'Artificial Intelligence & Data Science': r'\b(Data Science|Machine Learning|AI|Artificial Intelligence|Data Analysis|AI&DS|AIDS)\b',
        'Artificial Intelligence & Machine Learning': r'\b(Machine Learning|AI|Artificial Intelligence|ML)\b',
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
    cgpa_patterns = [
        r'\b(?:CGPA|GPA|Grade Point Average)\s*[:=]?\s*(\d+(?:\.\d+)?)\s*(?:/\s*(?:4|10))?',
        r'(?:obtained|secured|with|having|current|cumulative)?\s*(?:CGPA|GPA)\s*(?:of|:)?\s*(\d+(?:\.\d+)?)\s*(?:/\s*(?:4|10))?',
        r'(?:CGPA|GPA)\s*(?:-|:|\s)\s*(\d+(?:\.\d+)?)\s*(?:/\s*(?:4|10))?',
        r'(\d+(?:\.\d+)?)\s*/\s*(?:4|10)\s*(?:CGPA|GPA)',
    ]
    
    for pattern in cgpa_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                cgpa = float(match.group(1))
                # Normalize CGPA to 10-point scale
                if cgpa <= 4.0:
                    cgpa *= 2.5
                if 0 <= cgpa <= 10:
                    return round(cgpa, 2)
            except ValueError:
                continue
    return None

def extract_marks(text):
    marks_patterns = [
        r'\b(?:10th|X|SSC|Matriculation|12th|XII|HSC|Intermediate)\s*(?:standard|class)?(?:\s*-\s*|\s*:\s*|\s*percentage\s*:?\s*|\s*marks\s*:?\s*|\s*aggregate\s*:?\s*)(\d{2,3}(?:\.\d{1,2})?)\s*%?',
        r'(?:10th|X|SSC|Matriculation|12th|XII|HSC|Intermediate)\s*(?:standard|class)?.*?(\d{2,3}(?:\.\d{1,2})?)\s*%',
        r'(\d{2,3}(?:\.\d{1,2})?)\s*%\s*in\s*(?:10th|X|SSC|Matriculation|12th|XII|HSC|Intermediate)',
        r'(?:percentage|marks|aggregate)\s*in\s*(?:10th|X|SSC|Matriculation|12th|XII|HSC|Intermediate)\s*(?:-|:|\s)\s*(\d{2,3}(?:\.\d{1,2})?)\s*%?',
    ]
    
    marks_10th = None
    marks_12th = None
    
    for pattern in marks_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                marks = float(match.group(1))
                if 0 <= marks <= 100:
                    if '10' in match.group(0).lower() or 'x' in match.group(0).lower() or 'ssc' in match.group(0).lower() or 'matriculation' in match.group(0).lower():
                        marks_10th = marks
                    elif '12' in match.group(0).lower() or 'xii' in match.group(0).lower() or 'hsc' in match.group(0).lower() or 'intermediate' in match.group(0).lower():
                        marks_12th = marks
            except ValueError:
                continue

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
            cgpa = extract_cgpa(content)
            
            processed_data.append({
                'name': extract_name(content),
                'skills': extract_skills(content),
                'department': extract_department(content),
                'experience': extract_experience(content),
                'education': extract_education(content),
                'cgpa': cgpa if cgpa is not None else None,
                'marks_10th': marks_10th if marks_10th is not None else None,
                'marks_12th': marks_12th if marks_12th is not None else None
            })
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
