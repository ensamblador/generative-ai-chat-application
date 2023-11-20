from streamlit_cognito_auth import CognitoAuthenticator
import streamlit as st #all streamlit commands will be available through the "st" alias
import os


pool_id = os.environ.get("POOL_ID")
app_client_id = os.environ.get("APP_CLIENT_ID")
app_client_secret = os.environ.get("APP_CLIENT_SECRET")

is_logged_in =  False
auth_is_required = True if pool_id else False


if auth_is_required:
    authenticator = CognitoAuthenticator(
        pool_id=pool_id,
        app_client_secret=app_client_secret,
        app_client_id=app_client_id,
    )

    is_logged_in = authenticator.login()

def logout():
    authenticator.logout()

if (not is_logged_in) and auth_is_required :
    st.stop()


print ("Logged in:", is_logged_in, "Is Required:", auth_is_required)