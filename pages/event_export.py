import streamlit as st
import duckdb
import pandas as pd

st.title("Event Export")

# Connect to DuckDB
conn = duckdb.connect("motherduck.duckdb")

# Get list of events
events = conn.execute("SELECT id, event_name, date FROM events ORDER BY date DESC").fetchall()

if not events:
    st.info("No events found.")
    st.stop()

# Build event selection dropdown
event_labels = [f"{e[1]} ({e[2]})" for e in events]
event_map = {f"{e[1]} ({e[2]})": e[0] for e in events}
selected_label = st.selectbox("Select an Event", event_labels)
selected_event_id = event_map[selected_label]


# Query data to export
query = """
    SELECT 
        e.event_name,
        e.date,
        a.nickname,
        ag.group_name,
        si.split_name,
        s.split_time,
        ac.bib_number,
        ac.checkin_time,
        a.recorder_nickname,
    FROM split_times s
    LEFT JOIN events e ON s.event_id = e.id
    LEFT JOIN athletes a ON s.athlete_id = a.id
    LEFT JOIN athlete_groups ag ON a.group_id = ag.id
    LEFT JOIN athlete_checkins ac ON ac.athlete_id = a.id
    LEFT JOIN split_ids si ON si.id = s.split_id
    WHERE e.id = ?
    ORDER BY s.split_id, a.nickname
"""
df = conn.execute(query, [selected_event_id]).df()

# Show the data
st.subheader("Data being Exported")
st.dataframe(df)

# CSV download
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, file_name="event_export.csv", mime="text/csv")
