#Student page 
# import streamlit as st
# import google.generativeai as genai
# from st_circular_progress import CircularProgress
# from utils import process_single_pdf, extract_score_and_feedback
# from streamlit_extras.stylable_container import stylable_container

# # Configure generative AI with API key
# genai.configure(api_key='AIzaSyAxXbYg_t4nevMViIaEmCu55CGELs2UpO0')

# # Custom CSS for improved UI alignment
# STYLES = """
# <style>
# [data-testid="stAppViewContainer"] {
#   background: linear-gradient(135deg, #000000 30%, #2e2e70 100%);
#   background-size: cover;
# }
# [data-testid="stHeader"] {
#   background-color: rgba(0, 0, 0, 0) !important;
# }
# .student-heading {
#     font-size: 48px;
#     font-weight: bold;
#     margin-bottom: 30px;
#     color: white;
#     text-align: center;
# }
# .stButton > button {
#     height: 45px;
#     width: 100%;
#     background-color: #6A5ACD;
#     color: white;
#     padding: 15px;
#     border-radius: 10px;
#     border: none;
#     cursor: pointer;
#     margin: 10px 0;
#     font-size: 18px;
# }
# .stButton {
#     width: 60%;
#     margin: 0 auto; /* Center buttons */
# }
# .file-uploader {
#     background-color: #1a1a40;
#     padding: 20px;
#     border-radius: 10px;
#     margin-bottom: 20px;
#     color: white;
#     font-size: 16px;
# }
# .text-area {
#     background-color: #1a1a40;
#     padding: 20px;
#     border-radius: 10px;
#     color: white;
#     font-size: 16px;
#     width: 60%; 
#     margin: 0 auto; /* Center text area */
# }
# .result-box {
#     background-color: #1a1a40;
#     padding: 20px;
#     border-radius: 10px;
#     margin-top: 20px;
#     color: white;
# }
# </style>
# """

# # Function to generate AI response using Google Generative AI
# def generate_ai_response(prompt):
#     try:
#         model = genai.GenerativeModel('gemini-pro')
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"An error occurred: {str(e)}"

# # Function to create progress indicator for score
# def create_progress_indicator(score, key_prefix):
#     color = "red" if score < 70 else "yellow" if score < 85 else "green"
#     CircularProgress(
#         label="Match Score",
#         value=score,
#         key=f"{key_prefix}_score",
#         size="large",
#         color=color
#     ).st_circular_progress()
#     st.write(f"Score: {score}%")  # Ensuring the same score is displayed in text and graph

# # def student_function():
# #     st.markdown(STYLES, unsafe_allow_html=True)
    
# #     st.markdown("<h1 class='student-heading'>Student Resume Analysis</h1>", unsafe_allow_html=True)
    
# #     with stylable_container(key="resume_uploader", css_styles="file-uploader"):
# #         uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=['pdf', 'docx'])
    
# #     if uploaded_file:
# #         pdf_content = process_single_pdf(uploaded_file)
# #         with stylable_container(key="job_description", css_styles="text-area"):
# #             job_description = st.text_area("Enter the job description (at least 50 words)")
# #         jd_word_count = len(job_description.split())
        
# #         button_col, _ = st.columns([1, 1])
# #         with button_col:
# #             # Unique keys added for each button
# #             profile_btn = st.button("Profile Match Based on Job Description", key="profile_match_btn")
# #             keywords_btn = st.button("Find Missing Keywords", key="find_keywords_btn")
# #             improvise_btn = st.button("Improvise Resume", key="improvise_resume_btn")
# #             ats_btn = st.button("Calculate Total ATS", key="calculate_ats_btn")

# #         # Handling button actions below
# #         if profile_btn:
# #             if jd_word_count >= 50:
# #                 with st.spinner("ATS Checking..."):
# #                     response = generate_ai_response(
# #                         prompt=f"""You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches the job description. First the output should come as percentage and then keywords missing and last final thoughts.{job_description}{pdf_content}"""
# #                     )
# #                     score, feedback = extract_score_and_feedback(response)
                    
# #                     # Display both the text and circular progress graph for the same score
# #                     st.write(f"Overall Score: {score}/100")  # Ensure text matches graph
# #                     create_progress_indicator(score, "profile_match")
                    
# #                     # st.markdown(f"<div class='result-box'>{feedback}</div>", unsafe_allow_html=True)
# #             else:
# #                 st.warning("Please enter a job description with at least 50 words.")

# #         if keywords_btn:
# #             if jd_word_count >= 50:
# #                 with st.spinner("Finding missing keywords..."):
# #                     response = generate_ai_response(
# #                         prompt=f"""Identify keywords missing in the resume based on the job description given in the textbox and tell which skills are missing in the resume in the list form:\n{job_description}\nResume content:\n{pdf_content}"""
# #                     )
# #                     st.markdown(f"<div class='result-box'>{response}</div>", unsafe_allow_html=True)
# #             else:
# #                 st.warning("Please enter a job description with at least 50 words.")

# #         if improvise_btn:
# #             if jd_word_count >= 50:
# #                 with st.spinner("Suggesting improvements for the resume..."):
# #                     response = generate_ai_response(
# #                         prompt=f"""Suggest improvements for this resume based on the job description to increase the job profile and the ATS of the resume for the specific company and suggest courses that can be helpful for boosting the job value:\n{job_description}\nResume content:\n{pdf_content}"""
# #                     )
# #                     st.markdown(f"<div class='result-box'>{response}</div>", unsafe_allow_html=True)
# #             else:
# #                 st.warning("Please enter a job description with at least 50 words.")

# #         if ats_btn:
# #             with st.spinner("Calculating Grade..."):
# #                 response = generate_ai_response(
# #                     prompt=f"""You are a skilled ATS checker. Analyze the resume and give the percentage on a basis from 1 to 100 and check some parameters such as education, experience, skills, projects, certification, and if present, increase the score else decrease it. Job description: {job_description}. Resume content: {pdf_content}"""
# #                 )
                
# #                 # Display both textual score and graph
# #                 score, feedback = extract_score_and_feedback(response)
# #                 st.write(f"Overall Score: {score}/100")  # Ensure text matches graph
# #                 create_progress_indicator(score, "total_ats")
# #                 # st.markdown(f"<div class='result-box'>{feedback}</div>", unsafe_allow_html=True)   
# #     else:
# #         st.warning("Please upload a PDF or DOCX resume to proceed.")

# if __name__ == "__main__":
#     student_function()