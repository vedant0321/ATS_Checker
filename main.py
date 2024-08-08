import streamlit as st
from dotenv import load_dotenv
from streamlit_navigation_bar import st_navbar
from home import home
from student import student_function
from admin import admin_function
from contact import contact


load_dotenv()

# Main function to run the Streamlit app
def main():
    st.set_page_config(initial_sidebar_state="collapsed")
    page = ["Home", "Student", "Admin", "Contact"]
    styles = {
        "nav": {
            "background-color": "rgb(123, 209, 146)",
            #  "margin-top": "1.5rem",         
            },
        "div": {
            "max-width": "32rem",
        },
        "span": {
            "border-radius": "0.5rem",
            "color": "rgb(49, 51, 63)",
            "margin": "0 0.125rem",
            "padding": "0.4375rem 0.625rem",
        },
        "active": {
            "background-color": "rgba(255, 255, 255, 0.25)",
        },
        "hover": {
            "background-color": "rgba(255, 255, 255, 0.35)",
        },
    }
    page = st_navbar(page, styles=styles)
    
    
    
    if page == "Home":
        home()
    elif page == "Student":
        student_function()
    elif page == "Admin":
        admin_function()
    elif page == "Contact":
        contact()

if __name__ == "__main__":
    main()
