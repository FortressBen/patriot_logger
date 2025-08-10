import streamlit as st
from streamlit import session_state as ss
import streamlit_authenticator as stauth
import auth

st.header('Account page')

config = auth.get_config()
AUTHENTICATOR_STATUS_KEY="authentication_status"
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

login_tab, register_tab = st.tabs(['Login'])

with login_tab:
    r = authenticator.login(location='main')

    if ss[AUTHENTICATOR_STATUS_KEY]:
        authenticator.logout(location='main')
        st.write(f'Welcome *{ss["name"]}*')
    elif ss[AUTHENTICATOR_STATUS_KEY] is False:
        st.error('Username/password is incorrect')
    elif ss[AUTHENTICATOR_STATUS_KEY] is None:
        st.warning('Please enter your username and password')
