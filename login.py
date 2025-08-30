import streamlit as st
from datetime import datetime, timedelta
import time
import extra_streamlit_components as stx
from streamlit_js_eval import streamlit_js_eval
from app_secrets import SETTINGS
SECRETS_TOML_NAME="logins"
ADMIN_ROLE = 'ADMIN'
STUDENT_ROLE = 'STUDENT'
LOGIN_COOKIE_NAME = 'patriot_role37'
TEMP_SESSION_STATE_LOGIN = "just_logged_in"
cookie_manager = stx.CookieManager(key='patriot')
COOKIE_EXPIRE_DAYS = 1
expiry_date = datetime.now() + timedelta(days=COOKIE_EXPIRE_DAYS)

def _reload_page():
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

def log_out():
    #del st.session_state[LOGIN_COOKIE_NAME]
    #st.success("You are logged out.")
    #st.switch_page("home.py")
    #st.success("You are logged out.")
    #if st.session_state["LOGGING_OUT"] == True:
    try:
        cookie_manager.delete(LOGIN_COOKIE_NAME)
    except Exception as e:
        # stupid thing is buggy, throws an exeption but does delete the key
        print(f"inoring exception {e}")

    #this is important: it gives the websocket time to send the cookie
    time.sleep(1.5)


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

    just_logged_in_role = st.session_state.get(TEMP_SESSION_STATE_LOGIN,None)

    #cookie_role_cm = cookie_manager.get(cookie=LOGIN_COOKIE_NAME)
    context_role = st.context.cookies.get(LOGIN_COOKIE_NAME,None)

    if just_logged_in_role is not None :
        st.session_state[TEMP_SESSION_STATE_LOGIN] = None
        return just_logged_in_role
    else:
        return context_role

    #if LOGIN_COOKIE_NAME in st.session_state.keys():
    #    session_state_role = st.session_state[LOGIN_COOKIE_NAME]
    #else:
    #    session_state_role = None

    #return session_state_role

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
                        #st.session_state[LOGIN_COOKIE_NAME] = role
                        #st.success("You are Logged In.")
                        #st.switch_page("home.py")
                        cookie_manager.set(LOGIN_COOKIE_NAME,role,expires_at=expiry_date)
                        #this is important-- give time to send the cookie to the browser
                        time.sleep(1)
                        st.session_state[TEMP_SESSION_STATE_LOGIN] = role
                        _reload_page()
                        st.stop()
                else:
                    st.error("Password Doesnt match")
        st.stop()
    else:
        #user is logged in, return the users's role
        return get_user_role()




