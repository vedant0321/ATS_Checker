import streamlit as st
from firebase_config import get_user_data

def account_page():
    user = st.session_state.get("user", {})
    if user:
        # Fetch user data from Realtime Database
        user_data = get_user_data(user.get('localId', ''))

        # Safely handle missing user_data
        if user_data is None:
            st.warning("No additional user data found. Using default values.")
            user_data = {}  # Use an empty dictionary as a fallback

        st.title("Account Page")
        st.write(f"Name: {user_data.get('name', 'Not Provided')}")
        st.write(f"Email: {user_data.get('email', user.get('email', 'Not Provided'))}")
    else:
        st.error("User not logged in")

    if st.button("Logout"):
        st.session_state.clear()
        st.success("You have been logged out.")
        st.session_state["selected_page"] = "Home"
        st.rerun()

if __name__ == "__main__":
    account_page()
