import streamlit as st
import duckdb

st.title("Event Entry")

# Connect to DuckDB
conn = duckdb.connect("motherduck.duckdb")

# Ensure necessary tables exist
conn.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER,
    event_name TEXT,
    date TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS athlete_checkins (
    athlete_id INTEGER,
    event_id INTEGER,
    checkin_time TEXT,
    bib_number TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS athletes (
    id INTEGER,
    first_name TEXT,
    last_name TEXT,
    group_id INTEGER
)
""")

# Form to add a new event
with st.form("add_event_form"):
    event_name = st.text_input("Event Name")
    date = st.date_input("Event Date")
    submitted = st.form_submit_button("Add Event")

    if submitted:
        if not event_name.strip():
            st.error("Event name cannot be empty.")
        else:
            try:
                # Manually generate the next ID
                max_id_result = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM events").fetchone()
                next_id = max_id_result[0]

                # Insert new event with generated ID
                conn.execute(
                    "INSERT INTO events (id, event_name, date) VALUES (?, ?, ?)",
                    [next_id, event_name.strip(), date.isoformat()]
                )
                st.success(f"Event '{event_name}' added successfully!")
            except Exception as e:
                st.error(f"Error adding event: {e}")

# Show all current events
st.subheader("Current Events")

events_df = conn.execute("""
    SELECT 
        e.event_name AS "Event Name",
        e.date AS "Date",
        COUNT(ac.athlete_id) AS "Athletes Checked In"
    FROM events e
    LEFT JOIN athlete_checkins ac ON e.id = ac.event_id
    GROUP BY e.event_name, e.date
    ORDER BY e.date DESC
""").df()

if events_df.empty:
    st.info("No events have been added yet.")
else:
    st.dataframe(events_df, use_container_width=True)
