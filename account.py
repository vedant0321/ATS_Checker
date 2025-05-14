import streamlit as st
from firebase_config import get_user_data

def account_page():
    user = st.session_state.get("user", {})

    if not user or 'localId' not in user:
        st.error("User not logged in or session expired.")
        return

    # Get user data using the stored token if available
    id_token = user.get('idToken')
    user_data = get_user_data(user.get('localId', ''), id_token)

    if user_data is None:
        st.warning("No additional user data found. Using session data.")
        # Fall back to session state data if database retrieval fails
        user_data = {
            'name': user.get('name', 'Not Provided'),
            'email': user.get('email', 'Not Provided')
        }

    st.title("Account Page")

    with st.container(border=True):
        st.write(f":grey[Name] : {user_data.get('name', 'Not Provided')}")
        st.write(f":grey[Email] : {user_data.get('email', user.get('email', 'Not Provided'))}")

    if st.button("Logout"):
        st.session_state.clear()
        st.success("You have been logged out.")
        st.session_state["selected_page"] = "Home"
        st.rerun()

if __name__ == "__main__":
    account_page()