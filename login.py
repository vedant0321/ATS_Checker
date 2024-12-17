import streamlit as st
from firebase_config import auth_pyrebase, get_user_data
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
    
    /* Login button style */
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
    
    /* Signup text container */
    .signup-container {
        display: flex;
        align-items: center;
        gap: 5px;
        margin-top: 20px;
        justify-content: center;
    }
    
    .signup-text {
        color: #ffffff;
        margin: 0;
    }
    
    .signup-link {
        color: #7857FF;
        text-decoration: none;
        cursor: pointer;
        background: none;
        border: none;
        padding: 0;
        font: inherit;
    }
    
    .signup-link:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)
# Helper function to authenticate the user
def authenticate_user(email, password):
    try:
        user = auth_pyrebase.sign_in_with_email_and_password(email, password)
        user_data = get_user_data(user['localId'])
        if not user_data:
            # Handle the case where user data is not found
            st.warning("No additional user data found. Using default values.")
            user_data = {"name": "Unknown"}
        return user, user_data
    except Exception as e:
        error_message = str(e).lower()
        if "invalid password" in error_message:
            st.error("Invalid password. Please try again.")
        elif "invalid email" in error_message:
            st.error("Invalid email format. Please enter a valid email.")
        elif "user not found" in error_message:
            st.error("No account found with this email. Please check or sign up.")
        else:
            st.error(f"An error occurred: {e}")
        return None, None
# Function to manage the login page
def login_page():
    add_custom_css()
    
    col1, col2 = st.columns([1, 1], gap='medium')
    with col1:
        st.image("login.png", use_column_width=True)
    with col2:
        st.title("Login")
        
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        
        # Basic validation
        if st.button("Login"):
            if not email or not password:
                st.error("Both email and password are required.")
            else:
                user, user_data = authenticate_user(email, password)
                
                if user:
                    st.success(f"Logged in as {email}")
                    st.session_state["user"] = {
                        "localId": user['localId'],
                        "email": email,
                        "name": user_data.get('name', 'Not Provided')  # Default fallback
                    }
                    st.session_state["selected_page"] = "Student"  # Redirect to Student page
                    st.rerun()
        # Signup option
        col1, col2 = st.columns(2, gap="small")
        with col1:
            st.markdown('<p class="signup-text">Don\'t have an account?</p>', unsafe_allow_html=True)
        with col2:
            if st.button("Sign up here", key="signup_link"):
                st.session_state["selected_page"] = "Signup"
                st.rerun()
# Run the app
if __name__ == "__main__":
    login_page()

