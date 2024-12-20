import io
import re
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#student page
def process_single_pdf(uploaded_file):
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")

    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    return text

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
        "Critical Thinking", "Time Management","Flutter"
    ]
    found_skills = [skill for skill in skill_list if skill.lower() in text.lower()]
    return ", ".join(found_skills)

def extract_department(text):
    departments = {
        "Computer Branches": ["Information Technology", "Computer Technology", "IT", "Artificial intelligence and data science", "Artificial intelligence and machine learning", "computer science and design", "computer science and engineering", "computer science and mathematics", "computer science and physics", "computer science and statistics", "computer science and technology"],
        "Engineering": ["Engineering", "Mechanical", "Electrical"],
        "Marketing": ["Marketing", "Sales", "Advertising"],
        "Finance": ["Finance", "Accounting", "Banking"]
    }
    for dept, keywords in departments.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            return dept
    return "Other"

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


#admin page
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
