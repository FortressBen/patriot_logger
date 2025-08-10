import streamlit as st
from streamlit import session_state as ss
import yaml
from yaml.loader import SafeLoader

CONFIG_FILENAME = 'config.yaml'

def get_config():
    return None

def read_user_config():
    "read the config file, but then add secrets from secrets.toml"
    with open(CONFIG_FILENAME) as file:
        config = yaml.load(file, Loader=SafeLoader)


def get_roles():
    """Gets user roles based on config file."""
    with open(CONFIG_FILENAME) as file:
        config = yaml.load(file, Loader=SafeLoader)

    if config is not None:
        cred = config['credentials']
    else:
        cred = {}

    return {username: user_info['role'] for username, user_info in cred['usernames'].items() if 'role' in user_info}



AUTH_STATUS_KEY = 'authentication_status'
def check_logged_in():
    if AUTH_STATUS_KEY not in ss:
        st.switch_page('./pages/account.py')

    if AUTH_STATUS_KEY in ss.keys():
        if ss.get(AUTH_STATUS_KEY) is None:
            st.switch_page('./pages/account.py')


def get_role_for_user(username):
    if not username:
        return None

    """Gets user roles based on config file."""
    with open(CONFIG_FILENAME) as file:
        config = yaml.load(file, Loader=SafeLoader)

    if config is not None:
        cred = config['credentials']
    else:
        cred = {}

    return cred['usernames'][username].get('role',None)
    #return {username: user_info['role'] for username, user_info in cred['usernames'].items() if 'role' in user_info}