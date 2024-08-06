import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import PyPDF2
import re
import os
from dotenv import load_dotenv
import google.generativeai as genai
import plotly.graph_objects as go

# Load environment variables if using .env file
load_dotenv()

# Configure generative AI with API key
genai.configure(api_key='AIzaSyAdN9CPrHC7AH7yiI8Yh_8fGo8Knl97AcM')  # Replace with your actual API key

# Preprocessing functions
def process_single_pdf(uploaded_file):
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")

    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    return text

def process_multiple_pdfs(uploaded_files):
    processed_data = []

    for uploaded_file in uploaded_files:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        name = extract_name(text)
        skills = extract_skills(text)
        department = extract_department(text)
        experience = extract_experience(text)
        education = extract_education(text)

        processed_data.append({
            "name": name,
            "skills": skills,
            "department": department,
            "experience": experience,
            "education": education
        })

    return processed_data


# Function to create a gauge chart
def create_gauge_chart(value, max_value=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        gauge=dict(
            axis=dict(range=[0, max_value], tickcolor="black", ticklen=5, ticksuffix=""),
            bar=dict(color="royalblue"),
            bgcolor="lightgray",
            bordercolor="black",
            borderwidth=2,
            steps=[
                dict(range=[0, max_value * 0.5], color="lightgreen"),
                dict(range=[max_value * 0.5, max_value], color="lightcoral"),
            ],
        ),
        title={"text": "Resume ATS Score", "font": {"size": 24, "color": "black"}},
    ))
    fig.update_layout(
        paper_bgcolor="white",
        font=dict(size=20, color="black"),
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        width=400
    )
    return fig






def extract_score_and_feedback(result_text):
    # Initialize variables
    score = 0
    feedback = "No feedback available."
    
    # Try to extract score
    score_patterns = [
        r'(\d+)%',  # Matches "80%"
        r'(\d+)/100',  # Matches "80/100"
        r'(\d+) out of 100',  # Matches "80 out of 100"
        r'score of (\d+)',  # Matches "score of 80"
        r'rate this resume a (\d+)',  # Matches "rate this resume a 8"
    ]
    
    for pattern in score_patterns:
        match = re.search(pattern, result_text, re.IGNORECASE)
        if match:
            score = int(match.group(1))
            # If score is out of 10, convert to percentage
            if pattern.endswith('(\d+)') and score <= 10:
                score *= 10
            break
    
    # Try to extract feedback
    feedback_patterns = [
        r'(\d+)%\.?\s*(.+)',  # Matches "80%. The resume is..."
        r'Overall,?\s*(.+)',  # Matches "Overall, the resume is..."
        r'In summary,?\s*(.+)',  # Matches "In summary, the resume..."
        r'(?<=\n)(?!(\d+%|score:))(.+)',  # Matches any line that doesn't start with a score
    ]
    
    for pattern in feedback_patterns:
        match = re.search(pattern, result_text, re.DOTALL | re.IGNORECASE)
        if match:
            feedback = match.group(1) if len(match.groups()) == 1 else match.group(2)
            feedback = feedback.strip()
            break
    
    return score, feedback

def extract_name(text):
    match = re.search(r'^([A-Z][a-z]+ [A-Z][a-z]+)', text)
    return match.group(1) if match else "Unknown"

def extract_skills(text):
    skill_list = [
        "Python", "Java", "C++", "JavaScript", "HTML", "CSS", "SQL", "React", "Angular", "Node.js",
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
        "Critical Thinking", "Time Management"
    ]
    found_skills = [skill for skill in skill_list if skill.lower() in text.lower()]
    return ", ".join(found_skills)

def extract_department(text):
    departments = {
       "IT": ["Information Technology", "Computer Technology", "IT","Artificial intelligence and data science","Artificial intelligence and machine learning","computer science and design","computer science and engineering","computer science and mathematics","computer science and physics","computer science and statistics","computer science and technology"],
        "Engineering": ["Engineering", "Mechanical", "Electrical"],
        "Marketing": ["Marketing", "Sales", "Advertising"],
        "Finance": ["Finance", "Accounting", "Banking"]
    }
    for dept, keywords in departments.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            return dept
    return "Other"

def extract_experience(text):
    match = re.search(r'(\d+)\+?\s*years?\s*(?:of)?\s*experience', text, re.IGNORECASE)
    return int(match.group(1)) if match else 0

def extract_education(text):
    education_levels = ["PhD", "Master's", "Bachelor's", "Associate's"]
    for level in education_levels:
        if level.lower() in text.lower():
            return level
    return "Unknown"







# Analysis functions
def generate_summary_table(df):
    summary = df.groupby('department').agg({
        'name': 'count',
        'experience': 'mean',
        'skills': lambda x: ', '.join(set(', '.join(x).split(', ')))
    }).reset_index()
    summary.columns = ['Department', 'Candidates', 'Avg Experience', 'Skills']
    summary['Avg Experience'] = summary['Avg Experience'].round(1)
    return summary

def create_pie_chart(df, column):
    fig, ax = plt.subplots()
    df[column].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
    ax.set_title(f'{column.capitalize()} Distribution')
    return fig

def create_line_graph(df, x_column, y_column):
    fig, ax = plt.subplots()
    df.groupby(x_column)[y_column].mean().plot(kind='line', ax=ax)
    ax.set_title(f'{y_column.capitalize()} by {x_column.capitalize()}')
    ax.set_xlabel(x_column.capitalize())
    ax.set_ylabel(y_column.capitalize())
    return fig

def create_bar_graph(df, column):
    fig, ax = plt.subplots()
    df[column].value_counts().plot(kind='bar', ax=ax)
    ax.set_title(f'Candidates by {column.capitalize()}')
    ax.set_xlabel(column.capitalize())
    ax.set_ylabel('Number of Candidates')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# Admin page
def admin_function():
    st.title("Admin Dashboard")

    uploaded_files = st.file_uploader("Upload resumes (PDF only)", type=['pdf'], accept_multiple_files=True)

    if uploaded_files:
        processed_data = process_multiple_pdfs(uploaded_files)
        df = pd.DataFrame(processed_data)

        st.subheader("Summary Table")
        summary_table = generate_summary_table(df)
        st.table(summary_table)

        st.subheader("Visualizations")
        col1, col2 = st.columns(2)

        with col1:
            st.write("Skills Distribution")
            fig_pie = create_pie_chart(df, 'skills')
            st.pyplot(fig_pie)

            st.write("Experience by Department")
            fig_line = create_line_graph(df, 'department', 'experience')
            st.pyplot(fig_line)

        with col2:
            st.write("Candidates by Department")
            fig_bar = create_bar_graph(df, 'department')
            st.pyplot(fig_bar)

            st.write("Education Level Distribution")
            fig_pie_edu = create_pie_chart(df, 'education')
            st.pyplot(fig_pie_edu)

    else:
        st.warning("Please upload PDF resumes to proceed with analysis.")

# Student page
def student_function():
    st.title("Student Resume Analysis")

    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=['pdf','docx'])

    if uploaded_file:
        pdf_content = process_single_pdf(uploaded_file)

        job_description = st.text_area("Enter the job description")

        if st.button("ATS Check based on Job Description"):
            with st.spinner("ATS Checking..."):
                response = genai.generate_text(prompt=f"""You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches the job description. First the output should come as percentage and then keywords missing and last final thoughts.{job_description}{pdf_content}""")
                result_text = response.result # Assuming the response is structured with a 'result' key
                st.markdown(result_text)
            

        if st.button("Find Missing Keywords"):
            with st.spinner("Finding missing keywords..."):
                response = genai.generate_text(prompt=f"""Identify keywords missing in the resume based on the job description given in the textbox and tell which skill are missing in resume in the list form:\n{job_description}\nResume content:\n{pdf_content}""")
                result_text = response.result # Assuming the response is structured with a 'result' key
                st.markdown(result_text)

        if st.button("Improvise Resume"):
           with  st.spinner("Suggesting improvements for the resume..."): # Placeholder for future implementation
                response = genai.generate_text(prompt=f"""Suggest improvements for this resume based on the job description to increase the job profile:\n{job_description}\nResume content:\n{pdf_content}""")
                result_text = response.result # Assuming the response is structured with a 'result' key
                st.markdown(result_text)
        if st.button("Calculate Total ATS "):
            with st.spinner("Calculating Grade..."): 
                response = genai.generate_text(prompt=f"""You are a skilled ATS checker. Analyze the resume and give the percentage on basis from 1 t0 100 
                                               {job_description}Resume content:{pdf_content}""")
                result_text = response.result 
                st.markdown(result_text)
                score, feedback = extract_score_and_feedback(result_text)

                # Debug prints for extracted data
                st.write("Feedback:", feedback)
                st.write("Extracted Score:", score)

                        # Create and display the gauge chart
                fig_gauge = create_gauge_chart(score)
                st.plotly_chart(fig_gauge)

                        # Display feedback and score
                st.markdown(feedback)
                st.write(f"Score: {score}%")

    else:
        st.warning("Please upload a PDF resume to proceed.")

# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="Resume Analyzer", layout="wide")

    st.title("Resume Analyzer")

    st.write("Welcome to the Resume Analyzer application.")
    st.write("Please select a page from the sidebar:")
    st.write("- Student: Upload and analyze individual resumes")
    st.write("- Admin: Analyze multiple resumes and view statistics")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", ["Student", "Admin"])

    if page == "Student":
        student_function()
    elif page == "Admin":
        admin_function()

if __name__ == "__main__":
    main()
