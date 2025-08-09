import streamlit as st
from datetime import datetime, timedelta
import extra_streamlit_components as stx
from streamlit_js_eval import streamlit_js_eval

cookie_manager = stx.CookieManager()

SECRETS_TOML_NAME="logins"
ADMIN_ROLE = 'admin'
STUDENT_ROLE = 'student'

LOGIN_COOKIE_NAME = 'patriot_role31'
COOKIE_EXPIRE_DAYS = 1
expiry_date = datetime.now() + timedelta(days=COOKIE_EXPIRE_DAYS)

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
    cookie_role = cookie_manager.get(cookie=LOGIN_COOKIE_NAME)
    session_state_role = st.session_state.get('role',None)
    if cookie_role is not None:
        return cookie_role
    elif session_state_role is not None:
        return session_state_role
    else:
        return None

def check_logged_in():
    def _reload_page():
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

    def get_roles_dict():
        if st.secrets.has_key(SECRETS_TOML_NAME):
            return st.secrets.get(SECRETS_TOML_NAME)
        else:
            print("Secrets.toml not available. Using Defaults")
            return {
                'admin': 'admin',
                'student': 'student'
            }

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
                        cookie_manager.set(LOGIN_COOKIE_NAME,role)
                        st.session_state['role'] = role
                        _reload_page()
                else:
                    st.error("Password Doesnt match")
        st.stop()
    else:
        #user is logged in, return the users's role
        return get_user_role()




