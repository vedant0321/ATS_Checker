
import streamlit as st
import google.generativeai as genai
from st_circular_progress import CircularProgress
from utils import process_single_pdf, extract_score_and_feedback

# Configure generative AI with API key
genai.configure(api_key='AIzaSyAxXbYg_t4nevMViIaEmCu55CGELs2UpO0')

STYLES = """
<style>
[data-testid="stAppViewContainer"] {
  background: linear-gradient(135deg, #000000 30%, #2e2e70 100%);
}
[data-testid="stHeader"] {
  background-color: rgba(0, 0, 0, 0) !important;
}
.student-heading {
    font-size: 48px;
    font-weight: bold;
    margin-bottom: 30px;
    color: white;
    text-align: center;
}
.stButton > button {
    height: 45px;
    width: 100%;
    background-color: #6A5ACD;
    color: white;
    border-radius: 10px;
    font-size: 18px;
    margin: 10px 0;
}
.file-uploader, .text-area, .result-box {
    background-color: #1a1a40;
    padding: 20px;
    border-radius: 10px;
    color: white;
    font-size: 16px;
}
</style>
"""

def generate_ai_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def create_progress_indicator(score, key_prefix):
    color = "red" if score < 70 else "yellow" if score < 85 else "green"
    CircularProgress(
        label="Match Score",
        value=score,
        key=f"{key_prefix}_score_{st.session_state.get('counter', 0)}",  # Add unique key
        size="large",
        color=color
    ).st_circular_progress()

def student_function():
    st.markdown(STYLES, unsafe_allow_html=True)
    st.markdown("<h1 class='student-heading'>Student Resume Analysis</h1>", unsafe_allow_html=True)

    # Initialize session state variables
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    if 'results' not in st.session_state:
        st.session_state.results = {}

    # # Reset button
    # if st.button("Reset Analysis"):
    #     st.session_state.clear()
    #     st.experimental_rerun()

   
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=['pdf', 'docx'], key="resume_upload")
    
    if uploaded_file:
        pdf_content = process_single_pdf(uploaded_file)
        st.error("Upload Job description and then Press {crtl+enter}")
        job_description = st.text_area("Enter the job description", key="job_desc")

        if job_description:
            button_col1, button_col2 = st.columns(2)

            with button_col1:
                if st.button("Profile Match Based on Job Description", key="profile_match_btn"):
                    if len(job_description.split()) < 50:
                        st.warning("Please enter at least 50 words in the job description.")
                    else:
                        with st.spinner("Performing profile match..."):
                            response = generate_ai_response(
                                f"""Evaluate the resume against the job description. 
                                Provide the match percentage, missing keywords, and feedback. 
                                Job description: {job_description} 
                                Resume content: {pdf_content}"""
                            )
                            score, feedback = extract_score_and_feedback(response)
                            st.session_state.results['profile_match'] = {'score': score, 'feedback': feedback}
                            st.write(f"Profile Match Score: {score}/100")
                            create_progress_indicator(score, "profile_match")

            with button_col2:
                if st.button("Calculate Total ATS Score", key="calculate_ats_btn"):
                    if len(job_description.split()) < 50:
                        st.warning("Please enter at least 50 words in the job description.")
                    else:
                        with st.spinner("Calculating ATS score..."):
                            response = generate_ai_response(
                                f"""Analyze the resume for an overall ATS score (1 to 100). 
                                Consider education, skills, experience, and certifications. 
                                Job description: {job_description} 
                                Resume content: {pdf_content}"""
                            )
                            score, feedback = extract_score_and_feedback(response)
                            st.session_state.results['ats_score'] = {'score': score, 'feedback': feedback}
                            st.write(f"Total ATS Score: {score}/100")
                            create_progress_indicator(score, "ats")

            if 'profile_match' in st.session_state.results:
                if st.button("Find Missing Keywords", key="find_keywords_btn"):
                    with st.spinner("Finding missing skills..."):
                        response = generate_ai_response(
                            f"""Identify missing keywords and skills in the resume based on the provided job description. 
                            Job description: {job_description} 
                            Resume content: {pdf_content}"""
                        )
                        st.markdown(f"<div class='result-box'>{response}</div>", unsafe_allow_html=True)

                if st.button("Improvise Resume", key="improvise_resume_btn"):
                    with st.spinner("Generating resume improvement suggestions..."):
                        response = generate_ai_response(
                            f"""Suggest ways to improve the resume. Provide suggestions on relevant courses 
                            and strategies to enhance the profile and ATS score. 
                            Job description: {job_description} 
                            Resume content: {pdf_content}"""
                        )
                        st.markdown(f"<div class='result-box'>{response}</div>", unsafe_allow_html=True)

            st.session_state.counter += 1  # Increment counter for unique keys

    else:
        st.warning("Please upload your resume to proceed.")

if __name__ == "__main__":
    student_function()