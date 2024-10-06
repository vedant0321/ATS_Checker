import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

# Load environment variables if using .env file
load_dotenv()

from home import home
from student import student_function
from admin import admin_function
from contact import contact
import base64

def get_svg_base64(svg_path):
    with open(svg_path, "rb") as svg_file:
        svg_data = svg_file.read()
    return base64.b64encode(svg_data).decode()

def main():
    # Initialize session state for page selection
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Home"

    with st.sidebar:
        # Convert SVG to base64
        svg_base64 = get_svg_base64("logo.svg")
        
        # Display SVG using base64
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/svg+xml;base64,{svg_base64}" width="50">
            </div>
            """,
            unsafe_allow_html=True
        )

        selected = option_menu(
            menu_title="",
            options=["Home", "Student", "Admin", "Contact"],
            icons=["house", "backpack", "file-person", "telephone"],
            menu_icon="",
            default_index=["Home", "Student", "Admin", "Contact"].index(st.session_state.selected_page)
        )
        
        if selected != st.session_state.selected_page:
            st.session_state.selected_page = selected
            st.rerun()

    # Define functions to call based on selection
    page_functions = {
        "Home": home,
        "Student": student_function,
        "Admin": admin_function,
        "Contact": contact
    }

    # Call the corresponding function for the selected page
    page_functions[st.session_state.selected_page]()

if __name__ == "__main__":
    main()