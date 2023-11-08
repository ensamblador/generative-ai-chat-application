import os
# https://github.com/pop-srw/streamlit-cognito-auth
from streamlit_cognito_auth import CognitoAuthenticator




pool_id = os.environ.get("POOL_ID")
app_client_id = os.environ.get("APP_CLIENT_ID")
app_client_secret = os.environ.get("APP_CLIENT_SECRET")

is_logged_in =  False
auth_is_required = True if pool_id else False




authenticator = CognitoAuthenticator(
    pool_id=pool_id,
    app_client_secret=app_client_secret,
    app_client_id=app_client_id,
)

is_logged_in = authenticator.login()
    

def logout():
    authenticator.logout()

