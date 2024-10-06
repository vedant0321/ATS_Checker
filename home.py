import streamlit as st

# Background gradient and header style
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
  background: linear-gradient(135deg, #000000 30%, #1a1a40 100%);
  background-size: cover;
}

[data-testid="stHeader"] {
  background-color: rgba(0, 0, 0, 0) !important;
}
</style>
"""

# Main content style with glass effect
def home():
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown("""
    <style>
        .header {
            color: rgba(180, 120, 255, 0.7);
            font-size: 34px;
            margin-bottom: 20px;
        }
        .subheadings{
            color: white;
            font-size: 30px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .content {
            background-color: rgba(58, 58, 58, 0.3);
            padding: 20px;
            border-radius: 10px;
            display: flex;
            justify-content: space-evenly;
            align-items: center;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        .card {
            flex: 2;
        }
        .question {
            color: white;
            font-size: 44px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subtext {
            color: grey;
            font-size: 16px;
            margin-bottom: 20px;
        }
        .laptop img {
            width: 150px;
        }
        .stButton > button {
            height: 60px; /* Adjusted button height */
            background-color: #6A5ACD;
            color: white;
            font-size: 16px;
            padding: 15px 32px;
            border-radius: 30px;
            border: none;
            cursor: pointer;
            margin-top: 30px; /* Add space between the container and button */
            margin-bottom: 30px;
            display: flex; /* Center content horizontally */
            align-items: center; /* Center content vertically */
        }
        .stButton > button i {
            margin-right: 10px; /* Space between icon and text */
        }
    </style>
    """, unsafe_allow_html=True)

    # Header section
    st.markdown('<div class="header">Hello</div>', unsafe_allow_html=True)

    # Content section with glass effect and additional text
    st.markdown(
        """
        <div class="content">
            <div class="card">
                <div class="question">Is your resume good enough?</div>
                <div class="subtext">
                    We leverage advanced machine learning and AI models to empower students in creating optimized resumes, while helping administrators manage and analyze data more effectively.
                </div>
            </div>
            <div class="laptop">
                <img src="https://cdn.sanity.io/images/mz2hls6g/production/bc1c6ad069d2d26a8606816f0ed4a7c9c12c02b7-1200x801.jpg?w=3840&q=75&fit=clip&auto=format" alt="Laptop" style="max-width: 100%; height: auto;">
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add the "Get Started" button after the content
    if st.button("🚀 Get Started"):
        st.session_state.selected_page = "Student"
        st.rerun()
        
    st.markdown('<div class="subheadings">For Student</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtext">Our system provides personalized recommendations for improving resumes, ensuring they meet the standards of Applicant Tracking Systems (ATS) and job-specific criteria.</div>', unsafe_allow_html=True)

    # Popover functionality with matching style
    with st.popover("Overall ATS Evaluation                 "):
        st.markdown("Using fine-tuned machine learning models, we analyze resumes for general ATS compatibility, ensuring they align with industry standards.")
    with st.popover("Job Description-Specific ATS Evaluation"):
        st.markdown("Our specialized model compares resumes against specific job descriptions, providing detailed feedback and enhancement suggestions.")
    with st.popover("Resume Improvement Suggestions         "):
        st.markdown("We identify missing skills and experiences and offer actionable advice on how to strengthen resumes for better chances of success.")
    with st.popover("Customizable Resume Versions           "):
        st.markdown("Create and manage multiple resume versions, tailored to different job applications, with the help of AI-driven insights.")
    
    # Add the "→ Student" button
    if st.button("→ Student"):
        st.session_state.selected_page = "Student"
        st.rerun()

# Check if we need to redirect to the Student page
if 'selected_page' in st.session_state and st.session_state.selected_page == "Student":
    st.session_state.selected_page = "Student"
    st.rerun()
