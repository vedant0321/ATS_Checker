import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import os

# Constants
TEMPLATE_PATH = r"STT.docx"
IMAGE_PATH = r"ats.png"

# Styles
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
    .student-heading {
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 30px;
        color: white;
    }
    .nav-button {
        background-color: #6A5ACD;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin-top: 20px;
    }
    .stButton > button {
        height: 30px;
        background-color: #6A5ACD;
        color: white;
        padding: 15px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        margin-top: 10px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
    }
    .stButton > button i {
        margin-right: 10px;
    }
    </style>
    """,
    "card_style": """
    {
        background-color: #1a1a40;
        border-radius: 10px;
        padding: 20px;
        min-height: 50px;
        margin-bottom: 20px;
    }
    """
}

def load_docx_file(file_path):
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Template file not found at {file_path}")
        return None

def create_stylable_card(key, title, content):
    with stylable_container(key=key, css_styles=STYLES["card_style"]):
        expander = st.expander(title)
        with expander:
            st.write(content)

def add_section(title, cards):
    st.subheader(title)
    cols = st.columns(2)
    for i, (card_key, card_title, card_content) in enumerate(cards):
        with cols[i % 2]:
            create_stylable_card(card_key, card_title, card_content)

def navigation_button(label, page, unique_id):
    if st.button(label, key=f"{page.lower()}_{unique_id}_nav"):
        st.session_state.selected_page = page
        st.rerun()

def home():
    st.markdown(STYLES["page_bg_img"], unsafe_allow_html=True)

    with st.container(border=True):
        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.title("Is your resume good enough?")
            st.caption("AFIT leveraging technologies such as NLP and LLMs, and provides effective means for students to refine their resumes.")
            navigation_button("🚀 Get Started", "Student", "header")
        with col2:
            st.image(IMAGE_PATH, use_column_width=True)

    with stylable_container(key="resume_download", css_styles=STYLES["card_style"]):
        st.markdown("""
            <h3>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 10px;">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                </svg>
                Download Our Professional Resume Template
            </h3>
        """, unsafe_allow_html=True)
        st.caption("Get a head start with our professionally designed template!")
        
        docx_file = load_docx_file(TEMPLATE_PATH)
        if docx_file is not None:
            st.download_button(
                label="⬇️ Download Template",
                data=docx_file,
                file_name="Professional_Resume_Template.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    student_cards = [
        ("card1", "Overall ATS Evaluation", "Using fine-tuned machine learning models, we analyze resumes for general ATS compatibility..."),
        ("card2", "Job Description-Specific ATS Evaluation", "Our specialized model compares resumes against specific job descriptions..."),
        ("card3", "Resume Improvement Suggestions", "We identify missing skills and experiences and offer actionable advice..."),
        ("card4", "Customizable Resume Versions", "Create and manage multiple resume versions, tailored to different applications...")
    ]
    add_section("For Students", student_cards)
    navigation_button("🚀 Student Page", "Student", "footer")

    institution_cards = [
        ("inst_card1", "Multiple Resumes", "Efficiently manage and analyze multiple student resumes..."),
        ("inst_card2", "Visualization", "Gain insights through powerful data visualization..."),
        ("inst_card3", "Segmentation", "Segment and categorize resumes effectively...")
    ]
    add_section("For Institutions", institution_cards)
    navigation_button("🚀 Institution Page", "Admin", "footer")

def student_page():
    st.title("Student Page")
    st.write("This is the student page. Add your content here.")
    navigation_button("🏠 Back to Home", "Home", "student")

def admin_page():
    st.title("Admin Page")
    st.write("This is the admin page. Add your content here.")
    navigation_button("🏠 Back to Home", "Home", "admin")

def main():
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Home"

    page_functions = {
        "Home": home,
        "Student": student_page,
        "Admin": admin_page
    }

    page_functions[st.session_state.selected_page]()

if __name__ == "__main__":
    main()