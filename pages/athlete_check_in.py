import streamlit as st
import duckdb
from datetime import datetime

st.title("Athlete Check-In")

conn = duckdb.connect("motherduck.duckdb")

# Fetch events
events = conn.execute("SELECT id, event_name, date FROM events ORDER BY date DESC").fetchall()
if not events:
    st.warning("No events found. Please add events on the Event Entry page.")
    st.stop()

event_options = [f"{name} ({date})" for _, name, date in events]
selected_event_index = st.selectbox("Select Event", range(len(events)), format_func=lambda i: event_options[i])
selected_event_id = events[selected_event_index][0]

# Fetch athletes sorted by last name
athletes = conn.execute("""
    SELECT id, first_name, last_name
    FROM athletes
    ORDER BY last_name, first_name
""").fetchall()

if not athletes:
    st.warning("No athletes found. Please upload athletes first.")
    st.stop()

athlete_options = [f"{first} {last}" for _, first, last in athletes]
selected_athlete_index = st.selectbox("Select Athlete", range(len(athletes)), format_func=lambda i: athlete_options[i])
selected_athlete = athletes[selected_athlete_index]
selected_athlete_id = selected_athlete[0]
selected_athlete_name = f"{selected_athlete[1]} {selected_athlete[2]}"

# Bib number input
bib_number = st.text_input("Enter Bib Number (Optional)").strip()

# Check-in athlete
if st.button("Check In"):
    try:
        # Remove any existing check-in
        conn.execute("""
            DELETE FROM athlete_checkins
            WHERE athlete_id = ? AND event_id = ?
        """, (selected_athlete_id, selected_event_id))

        # Insert new check-in with updated bib number
        conn.execute("""
            INSERT INTO athlete_checkins (athlete_id, event_id, checkin_time, bib_number)
            VALUES (?, ?, ?, ?)
        """, (selected_athlete_id, selected_event_id, datetime.now().isoformat(), bib_number))

        st.success(f"{selected_athlete_name} checked in for event with bib number '{bib_number}'")

    except Exception as e:
        st.error(f"Error checking in athlete: {e}")
