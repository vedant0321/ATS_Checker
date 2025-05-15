# import firebase_admin
# from firebase_admin import credentials, auth, db
# import pyrebase

# # Initialize the Firebase Admin SDK with the service account key
# cred = credentials.Certificate("serviceAccountKey.json")

# # Check if Firebase Admin is already initialized
# try:
#     firebase_app = firebase_admin.get_app()
# except ValueError:
#     firebase_app = firebase_admin.initialize_app(cred, {
#         'databaseURL': 'https://afit-15355-default-rtdb.firebaseio.com'
#     })

# # Pyrebase configuration (for user sign-in and sign-up)
# firebase_config = {
#     "apiKey": "AIzaSyCzWLxei08ODPFqXddH1kisF8DqcdLZPQE",
#     "authDomain": "afit-15355.firebaseapp.com",
#     "databaseURL": "https://afit-15355-default-rtdb.firebaseio.com",
#     "projectId": "afit-15355",
#     "storageBucket": "afit-15355.appspot.com",
#     "messagingSenderId": "737169749315",
#     "appId": "1:737169749315:web:bdc13ece735ba831782bf6",
#     "measurementId": "G-1H8HK7ZXKD",
# }

# firebase = pyrebase.initialize_app(firebase_config)
# auth_pyrebase = firebase.auth()
# database = firebase.database()

# def save_user_data(user_id, name, email, id_token=None):
#     """
#     Save user data to Firebase Realtime Database.
#     If id_token is provided, it will use that token.
#     If not, it will try to use the current user's token if available.
#     """
#     try:
#         # If token is provided directly, use it
#         if id_token:
#             database.child("users").child(user_id).set({
#                 "name": name,
#                 "email": email
#             }, id_token)
#             return True
#         # Otherwise try to use current user's token
#         elif auth_pyrebase.current_user:
#             user_token = auth_pyrebase.current_user.get('idToken')
#             if user_token:
#                 database.child("users").child(user_id).set({
#                     "name": name,
#                     "email": email
#                 }, user_token)
#                 return True
#         # If no token is available, use admin SDK
#         else:
#             # Use Firebase Admin SDK instead
#             ref = firebase_admin.db.reference(f"/users/{user_id}")
#             ref.set({
#                 "name": name,
#                 "email": email
#             })
#             return True
#     except Exception as e:
#         print(f"Error saving user data: {str(e)}")
#         return False

# def get_user_data(user_id, id_token=None):
#     """
#     Get user data from Firebase Realtime Database.
#     If id_token is provided, it will use that token.
#     If not, it will try to use the current user's token if available.
#     """
#     try:
#         # If token is provided directly, use it
#         if id_token:
#             return database.child("users").child(user_id).get(id_token).val()
#         # Otherwise try to use current user's token
#         elif auth_pyrebase.current_user:
#             user_token = auth_pyrebase.current_user.get('idToken')
#             if user_token:
#                 return database.child("users").child(user_id).get(user_token).val()
#         # If no token is available, use admin SDK
#         else:
#             # Use Firebase Admin SDK instead
#             ref = firebase_admin.db.reference(f"/users/{user_id}")
#             return ref.get()
#     except Exception as e:
#         print(f"Error getting user data: {str(e)}")
#         return None

import streamlit as st
import firebase_admin
from firebase_admin import credentials, db, auth
import pyrebase
import json

# Check if Firebase Admin is already initialized
try:
    firebase_app = firebase_admin.get_app()
except ValueError:
    # Use secrets for Firebase Admin SDK initialization
    # For local development, using secrets.toml
    # For Streamlit Cloud, using the secrets you'll add in the dashboard
    service_account_info = st.secrets["firebase"]["service_account_key"]
    
    # Convert the service account info to a credentials object
    cred = credentials.Certificate(service_account_info)
    
    firebase_app = firebase_admin.initialize_app(cred, {
        'databaseURL': st.secrets["firebase"]["database_url"]
    })

# Pyrebase configuration (for user sign-in and sign-up)
firebase_config = {
    "apiKey": st.secrets["firebase"]["api_key"],
    "authDomain": st.secrets["firebase"]["auth_domain"],
    "databaseURL": st.secrets["firebase"]["database_url"],
    "projectId": st.secrets["firebase"]["project_id"],
    "storageBucket": st.secrets["firebase"]["storage_bucket"],
    "messagingSenderId": st.secrets["firebase"]["messaging_sender_id"],
    "appId": st.secrets["firebase"]["app_id"],
    "measurementId": st.secrets["firebase"]["measurement_id"],
}

firebase = pyrebase.initialize_app(firebase_config)
auth_pyrebase = firebase.auth()
database = firebase.database()

def save_user_data(user_id, name, email, id_token=None):
    """
    Save user data to Firebase Realtime Database.
    If id_token is provided, it will use that token.
    If not, it will try to use the current user's token if available.
    """
    try:
        # If token is provided directly, use it
        if id_token:
            database.child("users").child(user_id).set({
                "name": name,
                "email": email
            }, id_token)
            return True
        # Otherwise try to use current user's token
        elif auth_pyrebase.current_user:
            user_token = auth_pyrebase.current_user.get('idToken')
            if user_token:
                database.child("users").child(user_id).set({
                    "name": name,
                    "email": email
                }, user_token)
                return True
        # If no token is available, use admin SDK
        else:
            # Use Firebase Admin SDK instead
            ref = firebase_admin.db.reference(f"/users/{user_id}")
            ref.set({
                "name": name,
                "email": email
            })
            return True
    except Exception as e:
        st.error(f"Error saving user data: {str(e)}")
        return False

def get_user_data(user_id, id_token=None):
    """
    Get user data from Firebase Realtime Database.
    If id_token is provided, it will use that token.
    If not, it will try to use the current user's token if available.
    """
    try:
        # If token is provided directly, use it
        if id_token:
            return database.child("users").child(user_id).get(id_token).val()
        # Otherwise try to use current user's token
        elif auth_pyrebase.current_user:
            user_token = auth_pyrebase.current_user.get('idToken')
            if user_token:
                return database.child("users").child(user_id).get(user_token).val()
        # If no token is available, use admin SDK
        else:
            # Use Firebase Admin SDK instead
            ref = firebase_admin.db.reference(f"/users/{user_id}")
            return ref.get()
    except Exception as e:
        st.error(f"Error getting user data: {str(e)}")
        return None