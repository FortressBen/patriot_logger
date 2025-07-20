# home.py
import streamlit as st

st.set_page_config(
    page_title="JL Mann XC",
    page_icon="🏃‍♂️",
    layout="wide"
)

st.image("https://upload.wikimedia.org/wikipedia/en/7/77/JL_Mann_High_School_logo.png", width=200)
st.title("Welcome to the JL Mann Cross Country App")

st.markdown("""
### What would you like to do?
Use the sidebar to navigate:
- Upload athletes
- Log splits
- Manage events
- Run the master clock
""")
