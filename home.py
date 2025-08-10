import streamlit as st
from page_components import make_nav,make_header
from login import check_for_refresh

check_for_refresh()

st.set_page_config(
    page_title="JL Mann XC",
    page_icon="🏃‍♂️",
    layout="wide"
)
make_header("Welcome to the JL Mann Cross Country App")