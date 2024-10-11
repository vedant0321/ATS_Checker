import streamlit as st
import google.generativeai as genai
from st_circular_progress import CircularProgress
from utils import process_single_pdf, extract_score_and_feedback

# Configure generative AI with API key
genai.configure(api_key='AIzaSyAxXbYg_t4nevMViIaEmCu55CGELs2UpO0')

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
        key=f"{key_prefix}_score",
        size="large",
        color=color
    ).st_circular_progress()
    st.write(f"Score: {score}%")

def student_function():
    st.title("Student Resume Analysis")
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=['pdf', 'docx'])
    
    if uploaded_file:
        pdf_content = process_single_pdf(uploaded_file)
        job_description = st.text_area("Enter the job description")
        jd_word_count = len(job_description.split())

        if st.button("Profile Match Based on Job Description"):
            if jd_word_count >= 50:
                with st.spinner("ATS Checking..."):
                    response = generate_ai_response(
                        prompt=f"""You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches the job description. First the output should come as percentage and then keywords missing and last final thoughts.{job_description}{pdf_content}"""
                    )
                    score, feedback = extract_score_and_feedback(response)
                    create_progress_indicator(score, "profile_match")
                    # Display the detailed feedback
                    # st.markdown(response)
            else:
                st.warning("Please enter a job description with at least 50 words.")

        if st.button("Find Missing Keywords"):
            if jd_word_count >= 50:
                with st.spinner("Finding missing keywords..."):
                    response = generate_ai_response(
                        prompt=f"""Identify keywords missing in the resume based on the job description given in the textbox and tell which skills are missing in the resume in the list form:\n{job_description}\nResume content:\n{pdf_content}"""
                    )
                    st.markdown(response)
            else:
                st.warning("Please enter a job description with at least 50 words.")

        if st.button("Improvise Resume"):
            if jd_word_count >= 50:
                with st.spinner("Suggesting improvements for the resume..."):
                    response = generate_ai_response(
                        prompt=f"""Suggest improvements for this resume based on the job description to increase the job profile and the ats of the resume for the specific comapay and suggets course that can be helful for boosting the job value:\n{job_description}\nResume content:\n{pdf_content}"""
                    )
                    st.markdown(response)
            else:
                st.warning("Please enter a job description with at least 50 words.")

        if st.button("Calculate Total ATS"):
            with st.spinner("Calculating Grade..."):
                response = generate_ai_response(
                    prompt=f"""You are a skilled ATS checker. Analyze the resume and give the percentage on basis from 1 to 100 and check some parameters which are present or not such as education,experience,skill,projects,certification and if present increase the score else decrease{job_description}Resume content:{pdf_content}"""
                )
                st.write(response)
                
                score, feedback = extract_score_and_feedback(response)
                
                # Create and display the circular progress indicator for total ATS
                create_progress_indicator(score, "total_ats")

    else:
        st.warning("Please upload a PDF resume to proceed.")

if __name__ == "__main__":
    student_function()