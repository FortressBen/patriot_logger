import streamlit as st
from db import get_split_locations
from page_components import make_header
make_header("Split Groups")

st.info("""
Split groups are now hardcoded in the app as:
""")

split_ids = get_split_locations()

st.dataframe(split_ids,hide_index=True,width=200,)
