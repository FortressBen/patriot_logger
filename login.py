import streamlit as st
from datetime import datetime, timedelta
import extra_streamlit_components as stx
from streamlit_js_eval import streamlit_js_eval
import time

cookie_manager = stx.CookieManager(key='patriot')
SECRETS_TOML_NAME="logins"
ADMIN_ROLE = 'admin'
STUDENT_ROLE = 'student'

REQUEST_FULL_REFRESH = "REQUEST_FULL_REFRESH"

LOGIN_COOKIE_NAME = 'patriot_role37'
TEMP_SESSION_STATE_LOGIN = "just_logged_in"
COOKIE_EXPIRE_DAYS = 1
expiry_date = datetime.now() + timedelta(days=COOKIE_EXPIRE_DAYS)


def request_full_refresh():
    st.session_state[REQUEST_FULL_REFRESH] = True

def check_for_refresh():
    #This is a really shitty workaround because streamlits page controller is
    #broken in the case of handling cookies.
    if REQUEST_FULL_REFRESH in st.session_state.keys():

        del st.session_state[REQUEST_FULL_REFRESH]
        _reload_page()

def _reload_page():
    streamlit_js_eval(js_expressions="parent.window.location.reload()")


def log_out():
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

    #IMPORTANT NOTE!!!! using cookie_manager.get() has a bug-- it will return
    #cached values from the server when the cookie isnt in the client!!!
    #use st.conext.cookies instead to avoid this
    just_logged_in_role = st.session_state.get(TEMP_SESSION_STATE_LOGIN,None)

    #cookie_role_cm = cookie_manager.get(cookie=LOGIN_COOKIE_NAME)
    context_role = st.context.cookies.get(LOGIN_COOKIE_NAME,None)

    if just_logged_in_role is not None :
        st.session_state[TEMP_SESSION_STATE_LOGIN] = None
        return just_logged_in_role
    else:
        return context_role

    #if 'role' in st.session_state.keys():
    #    session_state_role = st.session_state['role']
    #else:
    #    session_state_role = None
    #print(f"Session state role={session_state_role}")
    #return session_state_role

def check_logged_in():


    def get_roles_dict():
        if st.secrets.has_key(SECRETS_TOML_NAME):
            return st.secrets.get(SECRETS_TOML_NAME)
        else:

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




