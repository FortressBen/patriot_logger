import streamlit as st
import pandas as pd
import duckdb as db

st.title("Export Event Splits")
con = db.connect("motherduck.duckdb")

df = con.execute("""
    SELECT e.event_name, a.first_name, a.last_name, s.name AS split, t.time_elapsed
    FROM split_times t
    JOIN athletes a ON a.id = t.athlete_id
    JOIN events e ON e.id = t.event_id
    JOIN split_ids s ON s.id = t.split_id
""").fetchdf()

st.download_button("Download CSV", df.to_csv(index=False), "event_splits.csv", "text/csv")
st.dataframe(df)