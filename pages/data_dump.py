import streamlit as st
import duckdb
import pandas as pd

st.title("Data Dump")

# Connect to DuckDB
conn = duckdb.connect("motherduck.duckdb")

a_df = conn.execute("SELECT * FROM athletes").df()
e_df = conn.execute("SELECT * FROM events").df()
ac_df = conn.execute("SELECT * FROM athlete_checkins").df()
ag_df = conn.execute("SELECT * FROM athlete_groups").df()
stime_df = conn.execute("SELECT * FROM split_times").df()
sid_df = conn.execute("SELECT * FROM split_ids").df()

st.subheader("Athletes")
st.dataframe(a_df)

st.subheader("Events")
st.dataframe(e_df)

st.subheader("Athlete Check-Ins")
st.dataframe(ac_df)

st.subheader("Athlete Groups")
st.dataframe(ag_df)

st.subheader("Split Times")
st.dataframe(stime_df)

st.subheader("Split Ids")
st.dataframe(sid_df)