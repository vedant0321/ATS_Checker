import io
import re
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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
        "IT": ["Information Technology", "Computer Technology", "IT", "Artificial intelligence and data science", "Artificial intelligence and machine learning", "computer science and design", "computer science and engineering", "computer science and mathematics", "computer science and physics", "computer science and statistics", "computer science and technology"],
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

def extract_score_and_feedback(result_text):
    score = 0
    feedback = "No feedback available."
    
    score_patterns = [
        r'(\d+)%',  
        r'(\d+)/100',  
        r'(\d+) out of 100',  
        r'score of (\d+)',  
        r'rate this resume a (\d+)',  
    ]
    
    for pattern in score_patterns:
        match = re.search(pattern, result_text, re.IGNORECASE)
        if match:
            score = int(match.group(1))
            if pattern.endswith('(\d+)') and score <= 10:
                score *= 10
            break
    
    feedback_patterns = [
        r'(\d+)%\.?\s*(.+)',  
        r'Overall,?\s*(.+)',  
        r'In summary,?\s*(.+)',  
        r'(?<=\n)(?!(\d+%|score:))(.+)',  
    ]
    
    for pattern in feedback_patterns:
        match = re.search(pattern, result_text, re.DOTALL | re.IGNORECASE)
        if match:
            feedback = match.group(1) if len(match.groups()) == 1 else match.group(2)
            feedback = feedback.strip()
            break
    
    return score, feedback

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
