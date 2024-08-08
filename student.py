import streamlit as st
import google.generativeai as genai
from utils import process_single_pdf, extract_score_and_feedback, create_gauge_chart

# Configure generative AI with API key
genai.configure(api_key='AIzaSyAdN9CPrHC7AH7yiI8Yh_8fGo8Knl97AcM')  # Replace with your actual API key

def student_function():
    st.title("Student Resume Analysis")

    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=['pdf', 'docx'])

    if uploaded_file:
        pdf_content = process_single_pdf(uploaded_file)

        job_description = st.text_area("Enter the job description")

        if st.button("ATS Check based on Job Description"):
            with st.spinner("ATS Checking..."):
                response = genai.generate_text(prompt=f"""You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches the job description. First the output should come as percentage and then keywords missing and last final thoughts.{job_description}{pdf_content}""")
                result_text = response.result  # Assuming the response is structured with a 'result' key
                st.markdown(result_text)
            
        if st.button("Find Missing Keywords"):
            with st.spinner("Finding missing keywords..."):
                response = genai.generate_text(prompt=f"""Identify keywords missing in the resume based on the job description given in the textbox and tell which skills are missing in the resume in the list form:\n{job_description}\nResume content:\n{pdf_content}""")
                result_text = response.result  # Assuming the response is structured with a 'result' key
                st.markdown(result_text)

        if st.button("Improvise Resume"):
            with st.spinner("Suggesting improvements for the resume..."): 
                response = genai.generate_text(prompt=f"""Suggest improvements for this resume based on the job description to increase the job profile:\n{job_description}\nResume content:\n{pdf_content}""")
                result_text = response.result  # Assuming the response is structured with a 'result' key
                st.markdown(result_text)

        if st.button("Calculate Total ATS"):
            with st.spinner("Calculating Grade..."): 
                response = genai.generate_text(prompt=f"""You are a skilled ATS checker. Analyze the resume and give the percentage on basis from 1 to 100 
                                               {job_description}Resume content:{pdf_content}""")
                result_text = response.result 
                st.markdown(result_text)
                score, feedback = extract_score_and_feedback(result_text)

                # Create and display the gauge chart
                fig_gauge = create_gauge_chart(score)
                st.plotly_chart(fig_gauge)

                st.write(f"Score: {score}%")

    else:
        st.warning("Please upload a PDF resume to proceed.")
