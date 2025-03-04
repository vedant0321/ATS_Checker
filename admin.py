import streamlit as st
import pandas as pd
import pdfplumber
import spacy
from spacy.matcher import Matcher
import re
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

# Load spaCy model
nlp = spacy.load("en_core_web_sm")
STYLES = {
    "page_bg_img": """
    <style>
    [data-testid="stAppViewContainer"] {
      background: linear-gradient(135deg, #000000 30%, #2e2e70 100%);
      background-size: cover;
    }
    [data-testid="stHeader"] {
      background-color: rgba(0, 0, 0, 0) !important;
    }
    """
}

@st.cache_data 
@st.cache_resource
def extract_text_from_pdf(file):
    """Extract text from PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text
    
# def process_multiple_pdfs(files):
#     processed_data = []
#     for file in files:
#         result = process_single_pdf(file)
#         if result:
#             processed_data.append(result)
#     return processed_data

######################################################  Name  ##################################################################

def extract_name(doc):
    """Extract name from first line or spaCy entities."""
    first_line = doc.text.strip().split('\n')[0]
    words = first_line.split()
    if 2 <= len(' '.join(words)) <= 30:
        return ' '.join(words)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Unknown"



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
# ######################################################  Email  ##################################################################


def extract_email(text):
    """Extract email using regex."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None
######################################################   Phone_Numbe #################################################################

def extract_phone_number(text):
    """Extract phone number using regex."""
    phone_pattern = r'\+?\d[\d -]{8,12}\d'
    match = re.search(phone_pattern, text)
    return match.group(0) if match else None
######################################################  Eduction  ##################################################################

def extract_degree(doc):
    """Extract degree using spaCy Matcher."""
    degree_patterns = {
        'PhD': [{"LOWER": {"IN": ["phd", "ph.d.", "doctor", "doctorate"]}}, {"LOWER": "of", "OP": "?"}, {"LOWER": "philosophy", "OP": "?"}],
        'Master': [{"LOWER": {"IN": ["master", "masters", "m.s.", "m.eng.", "mba"]}}],
        'Bachelor': [{"LOWER": {"IN": ["bachelor", "bachelors", "b.s.", "b.e.", "b.tech", "btech", "bachelor of technology", "b. tech"]}}]
    }
    matcher = Matcher(nlp.vocab)
    for level, pattern in degree_patterns.items():
        matcher.add(level, [pattern])
    matches = matcher(doc)
    for match_id, start, end in matches:
        return nlp.vocab.strings[match_id]
    return "Bachlor"

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
#     return "Bachlor"
###################################################### Department  ##################################################################

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

######################################################  CGPA  ##################################################################

# # def extract_cgpa(text):
# #     """Extract CGPA with flexible regex."""
# #     cgpa_pattern = r'(?:CGPA|GPA|cgpa|gpa|percent)[ :]*(\d+\.\d{1,2}|\d+)(?:/10)?'
# #     match = re.search(cgpa_pattern, text, re.IGNORECASE)
# #     if match:
# #         cgpa = float(match.group(1))
# #         # Normalize to 0-10 scale if percentage-like value
# #         if cgpa > 10 and cgpa <= 100:
# #             cgpa = cgpa / 10
# #         if 0 <= cgpa <= 10:
# #             return round(cgpa, 2)
# #     return None



def extract_cgpa(text):
    cgpa_pattern = r'\b(?:CGPA|GPA|cgpa|percent):\s*(\d+(?:\.\d+)?)\b'
    match = re.search(cgpa_pattern,text, re.IGNORECASE)
    if match:
        cgpa = float(match.group(1))
        if 0 <= cgpa <= 10:
            return round(cgpa, 2)
    return None
# ######################################################  Marks  ##################################################################

# def extract_marks(text):
#     """Extract 10th and 12th marks with robust context-aware regex."""
#     marks = {'ssc': None, 'hsc': None}
    
#     # Patterns for SSC (10th) and HSC (12th)
#     ssc_pattern = r'(?:ssc|10th|x|class x|cbse|secondary|matriculation)[ :,;\-\(\)]*(\d{1,2}(?:\.\d+)?)(?:%|\%|\\%|/100|/10)?'
#     hsc_pattern = r'(?:hsc|12th|xii|class xii|intermediate|senior secondary)[ :,;\-\(\)]*(\d{1,2}(?:\.\d+)?)(?:%|\%|\\%|/100|/10)?'
#     generic_pattern = r'(?:percentage|marks|grade)[ :]*\$?(\d{1,2}(?:\.\d+)?)(?:%|\%|\\%|/100|/10)?\$?'
    
#     # First pass: explicit context matching
#     ssc_match = re.search(ssc_pattern, text, re.IGNORECASE)
#     hsc_match = re.search(hsc_pattern, text, re.IGNORECASE)
    
#     if ssc_match:
#         marks['ssc'] = float(ssc_match.group(1))
#     if hsc_match:
#         marks['hsc'] = float(hsc_match.group(1))
    
#     # Second pass: generic percentage in education section
#     if not (marks['ssc'] and marks['hsc']):
#         lines = text.split('\n')
#         edu_section = False
#         percentages = []
#         for i, line in enumerate(lines):
#             if any(kw.lower() in line.lower() for kw in ['education', 'academic', 'ssc', 'hsc', '10th', '12th', 'x', 'xii']):
#                 edu_section = True
#                 # Look within next 5 lines for percentages
#                 for j in range(i, min(i + 5, len(lines))):
#                     generic_match = re.search(generic_pattern, lines[j], re.IGNORECASE)
#                     if generic_match:
#                         percentages.append(float(generic_match.group(1)))
#                     elif re.search(r'(\d{1,2}(?:\.\d+)?)(?:%|\%|\\%|/100|/10)', lines[j]):
#                         num = re.search(r'(\d{1,2}(?:\.\d+)?)', lines[j]).group(1)
#                         percentages.append(float(num))
#             elif edu_section and any(kw.lower() in line.lower() for kw in ['experience', 'projects', 'skills']):
#                 edu_section = False
#                 break
        
#         # Assign percentages based on order
#         if percentages and not marks['ssc'] and percentages[0] <= 100:
#             marks['ssc'] = percentages[0]
#         if len(percentages) > 1 and not marks['hsc'] and percentages[1] <= 100:
#             marks['hsc'] = percentages[1]
    
#     # Final validation
#     if marks['ssc'] and not (0 <= marks['ssc'] <= 100):
#         marks['ssc'] = None
#     if marks['hsc'] and not (0 <= marks['hsc'] <= 100):
#         marks['hsc'] = None
    
#     return marks['ssc'], marks['hsc']

def extract_marks(text):
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


######################################################  SkillS  ##################################################################


def extract_skills(doc):
    """Extract technical skills from predefined list."""
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
    return ', '.join(sorted(found_skills)) if found_skills else "None"

def extract_soft_skills(doc):
    """Extract soft skills with flexible matching."""
    soft_skills = set(["leadership", "team management", "communication", "teamwork", "problem solving", 
                       "critical thinking", "time management"])
    found_soft_skills = set()
    text_lower = doc.text.lower()
    for skill in soft_skills:
        if skill in text_lower:
            found_soft_skills.add(skill.title())
    return ', '.join(sorted(found_soft_skills)) if found_soft_skills else "None"
########################################################################################################################################
@st.cache_data 
@st.cache_resource
def process_single_pdf(file):
    """Process a single PDF file."""
    try:
        if file.type == "application/pdf":
            text = extract_text_from_pdf(file)
        else:
            text = file.getvalue().decode("utf-8")
        
        doc = nlp(text)
        
        return {
            'name': extract_name(doc),
            'email': extract_email(text),
            'phone_number': extract_phone_number(text),
            'degree': extract_degree(doc),
            'department': extract_department(doc),
            'cgpa': extract_cgpa(text),
            'marks_10th': extract_marks(text)[0],
            'marks_12th': extract_marks(text)[1],
            'tech_skills': extract_skills(doc),
            'soft_skills': extract_soft_skills(doc)
        }
    except Exception as e:
        st.error(f"Error processing file {file.name}: {str(e)}")
        return None

def process_multiple_pdfs(files):
    """Process multiple PDF files."""
    with ThreadPoolExecutor() as executor:
        processed_data = list(executor.map(process_single_pdf, files))
    return [data for data in processed_data if data is not None]

def create_dashboard(df):
    st.title("Dashboard")

    # Calculate averages first (excluding zeros and NaN values)
    valid_cgpa = df['cgpa'].dropna()
    avg_cgpa = valid_cgpa.mean() if not valid_cgpa.empty else 0
    
    valid_marks_10th = df['marks_10th'].dropna()
    avg_marks_10th = valid_marks_10th.mean() if not valid_marks_10th.empty else 0
    
    valid_marks_12th = df['marks_12th'].dropna()
    avg_marks_12th = valid_marks_12th.mean() if not valid_marks_12th.empty else 0
    
    # Replace NaN with calculated averages
    df['cgpa'] = df['cgpa']                         #.fillna(avg_cgpa)
    df['marks_10th'] = df['marks_10th']         #.fillna(avg_marks_10th)    
    df['marks_12th'] = df['marks_12th']         #.fillna(avg_marks_12th)

    # --- Filters ---
    st.sidebar.title("Filters")
    
    # Skills filter
    all_skills = set()
    for skills in df['tech_skills'].str.split(', '):
        if isinstance(skills, list):
            all_skills.update(skills)
    all_skills.discard('None')  # Remove 'None' from filter options
    selected_skills = st.sidebar.multiselect('Filter by Skills', sorted(all_skills))
    
    # Department filter
    departments = df['degree'].unique()
    selected_departments = st.sidebar.multiselect('Filter by Department', departments)
    
    # CGPA range filter
    cgpa_min, cgpa_max = float(df['cgpa'].min()), float(df['cgpa'].max())
    cgpa_range = st.sidebar.slider('CGPA Range', cgpa_min, cgpa_max, (cgpa_min, cgpa_max))
    
    # 10th and 12th percentage range filters
    marks_10th_min, marks_10th_max = float(df['marks_10th'].min()), float(df['marks_10th'].max())
    marks_10th_range = st.sidebar.slider('10th Percentage Range', marks_10th_min, marks_10th_max, (marks_10th_min, marks_10th_max))
    
    marks_12th_min, marks_12th_max = float(df['marks_12th'].min()), float(df['marks_12th'].max())
    marks_12th_range = st.sidebar.slider('12th Percentage Range', marks_12th_min, marks_12th_max, (marks_12th_min, marks_12th_max))

    # --- Apply Filters ---
    filtered_df = df.copy()
    if selected_skills:
        filtered_df = filtered_df[filtered_df['tech_skills'].apply(lambda x: any(skill in x.split(', ') for skill in selected_skills) if isinstance(x, str) else False)]
    if selected_departments:
        filtered_df = filtered_df[filtered_df['degree'].isin(selected_departments)]
    filtered_df = filtered_df[
        (filtered_df['cgpa'].between(cgpa_range[0], cgpa_range[1], inclusive='both')) &
        (filtered_df['marks_10th'].between(marks_10th_range[0], marks_10th_range[1], inclusive='both')) &
        (filtered_df['marks_12th'].between(marks_12th_range[0], marks_12th_range[1], inclusive='both'))
    ]

    # --- Row 1: KPIs ---
    col1, col2, col3 = st.columns(3, gap= 'large')
    
    with col1:
        with st.container(border=True):
           st.metric("Total Students", len(filtered_df))
    with col2:
        with st.container(border=True):
           avg_cgpa = filtered_df['cgpa'].mean() if not filtered_df.empty else 0
           st.metric("Average CGPA", f"{avg_cgpa:.2f}")
    with col3:
        with st.container(border=True):
           all_skills = [skill for skills in filtered_df['tech_skills'].str.split(', ') if isinstance(skills, list) for skill in skills if skill != 'None']
           top_skill = Counter(all_skills).most_common(1)[0][0] if all_skills else "N/A"
           st.metric("Top Skill", top_skill)

    # --- Row 2: Skills Distribution and CGPA Distribution ---
    col1, col2 = st.columns([2,1])
    
    with col1:
        with st.container(border=True):
           skills_count = Counter(all_skills)
           skills_df = pd.DataFrame.from_dict(skills_count, orient='index').reset_index()
           skills_df.columns = ['Skill', 'Count']
           fig_skills = px.line(skills_df.sort_values('Count', ascending=False).head(10), x='Skill', y='Count', title='Top 10 Technical Skills')
           st.plotly_chart(fig_skills, use_container_width=True)
    
    with col2:
        with st.container(border=True):
           cgpa_ranges = pd.cut(filtered_df['cgpa'], bins=[0, 6, 7, 8, 9, 10], labels=['<6', '6-7', '7-8', '8-9', '9-10'])
           cgpa_dist = cgpa_ranges.value_counts().sort_index()
           fig_cgpa = go.Figure(data=[go.Pie(labels=cgpa_dist.index, values=cgpa_dist.values, hole=.3)])
           fig_cgpa.update_layout(title='CGPA Distribution')
           st.plotly_chart(fig_cgpa, use_container_width=True)

    # --- Row 3: Soft Skills and Marks Distribution ---

    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
           soft_skills = [skill for skills in filtered_df['soft_skills'].str.split(', ') if isinstance(skills, list) for skill in skills if skill != 'None']
           soft_skills_count = Counter(soft_skills)
           fig_soft = px.bar(x=list(soft_skills_count.keys()), y=list(soft_skills_count.values()), title='Soft Skills Distribution')
           st.plotly_chart(fig_soft, use_container_width=True)
    
    with col2:
        with st.container(border=True):
           marks_10th_bins = pd.cut(filtered_df['marks_10th'], bins=[0, 60, 70, 80, 90, 100], labels=['<60', '60-70', '70-80', '80-90', '90-100'])
           marks_10th_dist = marks_10th_bins.value_counts().sort_index()
           fig_10th = px.pie(names=marks_10th_dist.index, values=marks_10th_dist.values, title='10th Percentage Distribution')
           st.plotly_chart(fig_10th, use_container_width=True)
    
    with col3:
        with st.container(border=True):
           marks_12th_bins = pd.cut(filtered_df['marks_12th'], bins=[0, 60, 70, 80, 90, 100], labels=['<60', '60-70', '70-80', '80-90', '90-100'])
           marks_12th_dist = marks_12th_bins.value_counts().sort_index()
           fig_12th = px.pie(names=marks_12th_dist.index, values=marks_12th_dist.values, title='12th Percentage Distribution')
           st.plotly_chart(fig_12th, use_container_width=True)

    # --- Filtered Students Table ---
    st.markdown("### Filtered Students")
    display_df = filtered_df[['name','email','phone_number' ,'degree', 'cgpa','department', 'marks_10th', 'marks_12th', 'tech_skills', 'soft_skills']]
    st.dataframe(display_df.style.format({'Phone_Number': "{:l}",'cgpa': "{:.2f}", 'marks_10th': "{:.2f}", 'marks_12th': "{:.2f}"}))

    # --- Export Filtered Data ---
    if st.button("Export Filtered Data to CSV"):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Filtered CSV",
            data=csv,
            file_name="filtered_resume_data.csv",
            mime="text/csv",
        )

def admin_function():
    st.markdown(STYLES["page_bg_img"], unsafe_allow_html=True)

    st.title("Interactive Resume Analyzer")
    
    uploaded_files = st.file_uploader("Upload resumes (PDF, TXT)", type=['pdf', 'txt'], accept_multiple_files=True)
    
    if uploaded_files:
        with st.spinner('Processing resumes...'):
            processed_data = process_multiple_pdfs(uploaded_files)
        df = pd.DataFrame(processed_data)
        
        if not df.empty:
            create_dashboard(df)
        else:
            st.warning("No data extracted from the resumes.")
    else:
        st.warning("Please upload PDF or TXT resumes to proceed with extraction.")

if __name__ == "__main__":
    admin_function()