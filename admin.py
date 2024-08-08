import streamlit as st
import pandas as pd
from utils import process_multiple_pdfs, generate_summary_table, create_pie_chart, create_line_graph, create_bar_graph

def admin_function():
    st.title("Admin Dashboard")

    uploaded_files = st.file_uploader("Upload resumes (PDF only)", type=['pdf'], accept_multiple_files=True)

    if uploaded_files:
        processed_data = process_multiple_pdfs(uploaded_files)
        df = pd.DataFrame(processed_data)

        st.subheader("Summary Table")
        summary_table = generate_summary_table(df)
        st.table(summary_table)

        st.subheader("Visualizations")
        col1, col2 = st.columns(2)

        with col1:
            st.write("Skills Distribution")
            fig_pie = create_pie_chart(df, 'skills')
            st.pyplot(fig_pie)

            st.write("Experience by Department")
            fig_line = create_line_graph(df, 'department', 'experience')
            st.pyplot(fig_line)

        with col2:
            st.write("Candidates by Department")
            fig_bar = create_bar_graph(df, 'department')
            st.pyplot(fig_bar)

            st.write("Education Level Distribution")
            fig_pie_edu = create_pie_chart(df, 'education')
            st.pyplot(fig_pie_edu)

    else:
        st.warning("Please upload PDF resumes to proceed with analysis.")
