'''import duckdb
import streamlit as st
import duckdb as db

st.title("Manage Athlete Groups")
con = duckdb.connect("motherduck.duckdb")

with st.form("add_group"):
    group_name = st.text_input("Group Name (e.g. Varsity)")
    submitted = st.form_submit_button("Add Group")
    if submitted:
        con.execute("INSERT INTO athlete_groups (group_name) VALUES (?)", (group_name,))
        st.success(f"Added group '{group_name}'")

groups = con.execute("SELECT * FROM athlete_groups").fetchall()
st.write(groups)'''

import streamlit as st

st.title("Split Groups")

st.info("""
Split groups are now hardcoded in the app as:

- 1: 0.5 mile  
- 2: 1 mile  
- 3: 2 mile  
- 4: 2.6 mile  
- 5: Final

There is no dynamic editing for split groups.
""")