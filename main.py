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

def main():
    with st.sidebar:
        # Test with a default icon first
        selected = option_menu(
            menu_title="AFIT",
            options=["Home", "Student", "Admin", "Contact"],
            icons=["house", "backpack", "file-person", "telephone"],  # Default icons
            menu_icon="✨",
            default_index=0
        )
        
        # Apply custom icon if it works with default icon
        # Uncomment the below line and comment out the default line if it works
        # selected = option_menu(
        #     menu_title="",
        #     options=["Home", "Student", "Admin", "Contact"],
        #     icons=["house", "backpack", "file-person", "telephone"],
        #     menu_icon="C:\\Users\\om wanjari\\Desktop\\my\\logo.svg",
        #     default_index=0
        # )

    page_functions = {
        "Home": home,
        "Student": student_function,
        "Admin": admin_function,
        "Contact": contact
    }

    if selected in page_functions:
        page_functions[selected]()
    else:
        st.error("Invalid selection")  # Error handling for unexpected values

if __name__ == "__main__":
    main()
