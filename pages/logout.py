import streamlit as st
from login import log_out,request_full_refresh

log_out()
request_full_refresh()
st.switch_page("home.py")


