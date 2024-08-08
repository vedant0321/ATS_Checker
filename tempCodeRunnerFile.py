import streamlit as st
import pandas as pd
from utils import process_multiple_pdfs 
def admin_function():
    st.title("Admin Dashboard")

    uploaded_files = st.file_uploader("Upload resumes (PDF only)", type=['pdf'], accept_multiple_files=True)

    if uploaded_files:
        processed_data = process_multiple_pdfs(uploaded_files)
        df = pd.DataFrame(processed_data)

    else:
        st.warning("Please upload PDF resumes to proceed with analysis.")
