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
    return 0  # Default to 0 if no experience found


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
        'Computer Sciencen and design': r'\b(CSD|computer science and design)\b',
    }
    for dept, pattern in departments.items():
        if re.search(pattern, text, re.IGNORECASE):
            return dept
    return "Other"

def extract_skills(text):
    skills = set( ["Python", "Java", "C++", "JavaScript", "HTML", "CSS", "SQL", "React", "Angular", "Node.js",
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

def process_single_pdf(file):
    if file.type == "application/pdf":
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    else:
        text = file.getvalue().decode("utf-8")
    return text

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
        
        # Experience filter
        max_experience = int(df['experience'].max())

        if max_experience > 0:
            exp_range = st.sidebar.slider(
                "Select Experience Range (years)", 
                min_value=0, 
                max_value=max_experience,
                value=(0, max_experience)
            )
        else:
            st.sidebar.write("All candidates have 0 years of experience.")
            exp_range = (0, 0)  # Default range when all experience is 0

        # Skills filter
        all_skills = set(','.join(df['skills']).replace(', ', ',').split(','))
        selected_skills = st.sidebar.multiselect("Select Skills", options=list(all_skills))
        
        # Department filter
        departments = df['department'].unique()
        selected_departments = st.sidebar.multiselect("Select Departments", options=departments, default=departments)
        
        # Education filter
        education_levels = df['education'].unique()
        selected_education = st.sidebar.multiselect("Select Education Levels", options=education_levels, default=education_levels)

        # Apply filters
        mask = (df['experience'].between(exp_range[0], exp_range[1])) & \
               (df['department'].isin(selected_departments)) & \
               (df['education'].isin(selected_education))
        
        if selected_skills:
            mask &= df['skills'].apply(lambda x: any(skill in x for skill in selected_skills))

        filtered_df = df[mask]

        # Display filtered data
        st.subheader("Filtered Resume Data")
        st.dataframe(filtered_df)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Experience Distribution")
            fig_exp = px.histogram(filtered_df, x='experience', nbins=10,
                                   title='Experience Distribution',
                                   labels={'experience': 'Years of Experience', 'count': 'Number of Candidates'})
            st.plotly_chart(fig_exp, use_container_width=True)

        with col2:
            st.subheader("Department Distribution")
            fig_dept = px.pie(filtered_df, names='department', title='Departments')
            st.plotly_chart(fig_dept, use_container_width=True)

        st.subheader("Skills Breakdown")
        skills_count = filtered_df['skills'].str.split(', ').explode().value_counts()
        fig_skills = px.bar(skills_count, x=skills_count.index, y=skills_count.values,
                            title='Top Skills',
                            labels={'index': 'Skills', 'value': 'Count'})
        st.plotly_chart(fig_skills, use_container_width=True)

        st.subheader("Education vs Experience")
        fig_edu_exp = px.scatter(filtered_df, x='experience', y='education', color='department',
                                 title='Education vs Experience',
                                 labels={'experience': 'Years of Experience', 'education': 'Education Level'})
        st.plotly_chart(fig_edu_exp, use_container_width=True)

        st.subheader("Candidate Details")
        for _, row in filtered_df.iterrows():
            with st.expander(f"{row['name']} - {row['department']}"):
                st.write(f"Experience: {row['experience']} years")
                st.write(f"Education: {row['education']}")
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
        st.warning("Please upload PDF or TXT resumes to proceed with analysis.")

if __name__ == "__main__":
    admin_function()


