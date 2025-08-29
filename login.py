import streamlit as st
from datetime import datetime, timedelta
import time
from app_secrets import SETTINGS
SECRETS_TOML_NAME="logins"
ADMIN_ROLE = 'ADMIN'
STUDENT_ROLE = 'STUDENT'
LOGIN_COOKIE_NAME = 'patriot_role37'

def log_out():
    del st.session_state[LOGIN_COOKIE_NAME]
    st.success("You are logged out.")
    st.switch_page("home.py")

def is_logged_in():
    return get_user_role() is not None

def require_any_role():
    user_role = check_logged_in()
    if user_role is None:
        st.warning("You cannot Do much Here.")
        st.stop()

def require_student():
    require_role(STUDENT_ROLE)

def require_admin():
    require_role(ADMIN_ROLE)

def require_role(required_role: str):
    user_role = check_logged_in()

    if user_role != required_role:
        st.warning("You cannot Do much Here.")
        st.stop()

def get_user_role():

    if LOGIN_COOKIE_NAME in st.session_state.keys():
        session_state_role = st.session_state[LOGIN_COOKIE_NAME]
    else:
        session_state_role = None

    return session_state_role

def check_logged_in():


    def get_roles_dict():
        return SETTINGS["LOGINS"]
        # if st.secrets.has_key(SECRETS_TOML_NAME):
        #     return st.secrets.get(SECRETS_TOML_NAME)
        # else:
        #
        #     return {
        #         'admin': 'admin',
        #         'student': 'student'
        #     }

    if not is_logged_in():
        #display Login banner
        st.title("Please Authenticate")
        with st.form("login_form"):
            supplied_password = st.text_input("Please Enter Password")
            submitted = st.form_submit_button("Login")

            if submitted:
                role_dict = get_roles_dict()
                for role,right_password in role_dict.items():
                    if right_password == supplied_password:
                        st.session_state[LOGIN_COOKIE_NAME] = role
                        st.success("You are Logged In.")
                        st.switch_page("home.py")
                else:
                    st.error("Password Doesnt match")
        st.stop()
    else:
        #user is logged in, return the users's role
        return get_user_role()




