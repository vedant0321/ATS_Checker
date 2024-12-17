import streamlit as st
from firebase_config import auth_pyrebase, save_user_data

# Helper function to add custom CSS styles
def add_custom_css():
    st.markdown("""
    <style>
    /* Background gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #000000 30%, #2e2e70 100%);
        background-size: cover;
    }
    
    /* Remove header background */
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0) !important;
    }
    
    /* Signup button style */
    .stButton > button {
        background-color: #7857FF;
        color: white;
        padding: 5px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        width: 100%;
        margin-top: 5px;
    }
    
    /* Input field styles */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper function to create a new user
def create_new_user(email, password, name):
    try:
        # Create user using Firebase authentication
        user = auth_pyrebase.create_user_with_email_and_password(email, password)
        # Save user data to the database
        save_user_data(user['localId'], name, email)
        return user
    except Exception as e:
        error_message = str(e).lower()
        if "email already in use" in error_message:
            st.error("This email is already in use. Please log in or use another email.")
        elif "weak password" in error_message:
            st.error("Password should be at least 6 characters.")
        elif "invalid email" in error_message:
            st.error("Please enter a valid email address.")
        else:
            st.error(f"An error occurred: {e}")
        return None

# Function to manage the signup page
def signup_page():
    add_custom_css()
    
    col1, col2 = st.columns([1, 1], gap='medium', vertical_alignment="center")

    with col1:
        st.image("signin.png", use_column_width=True)
    
    with col2:
        st.title("Sign Up")

        name = st.text_input("Name", placeholder="Enter your name")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Enter your password", type="password")

        # Basic validation
        if st.button("Sign Up"):
            if not name or not email or not password:
                st.error("All fields (Name, Email, Password) are required.")
            else:
                user = create_new_user(email, password, name)
                if user:
                    st.success("Account created successfully!")
                    st.session_state["user"] = {
                        "localId": user['localId'],
                        "email": email,
                        "name": name
                    }
                    st.session_state["selected_page"] = "Student"
                    st.rerun()

        # Redirect to login
        col1, col2 = st.columns(2)
        with col1:
            st.write("Already have account?")
        with col2:
            if st.button("Login here", key="login_link"):
                st.session_state["selected_page"] = "Login"
                st.rerun()

# Run the app
if __name__ == "__main__":
    signup_page()
