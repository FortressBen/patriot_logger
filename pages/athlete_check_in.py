import streamlit as st
import duckdb
from datetime import datetime

st.title("Athlete Check-In")

conn = duckdb.connect("motherduck.duckdb")

# Load events sorted by date descending
events = conn.execute("""
    SELECT id, event_name, date FROM events ORDER BY date DESC
""").fetchall()

if not events:
    st.warning("No events found. Please add events first.")
    st.stop()

event_options = [f"{name} ({date})" for _, name, date in events]
selected_event_index = st.selectbox("Select Event", range(len(event_options)), format_func=lambda i: event_options[i])
selected_event_id = events[selected_event_index][0]

# Load athletes sorted alphabetically by last name, then first name
athletes = conn.execute("""
    SELECT id, first_name, last_name FROM athletes ORDER BY last_name ASC, first_name ASC
""").fetchall()

if not athletes:
    st.warning("No athletes found. Please upload athletes first.")
    st.stop()

athlete_options = [f"{first} {last}" for _, first, last in athletes]
selected_athlete_index = st.selectbox("Select Athlete by Name", range(len(athlete_options)), format_func=lambda i: athlete_options[i])
selected_athlete = athletes[selected_athlete_index]
athlete_id = selected_athlete[0]

# Bib number input (optional, per event)
bib_input = st.text_input("Enter Bib Number for this Event (optional)")

if st.button("Check In Athlete"):
    bib_stripped = bib_input.strip()

    # Check if athlete is already checked in for this event
    existing_checkin = conn.execute("""
        SELECT 1 FROM athlete_checkins WHERE athlete_id = ? AND event_id = ?
    """, (athlete_id, selected_event_id)).fetchone()

    if existing_checkin:
        st.warning(f"{selected_athlete[1]} {selected_athlete[2]} is already checked in for this event.")
    else:
        now_str = datetime.now().isoformat()
        try:
            conn.execute("""
                INSERT INTO athlete_checkins (athlete_id, event_id, checkin_time, bib_number)
                VALUES (?, ?, ?, ?)
            """, (athlete_id, selected_event_id, now_str, bib_stripped if bib_stripped else None))
            st.success(f"{selected_athlete[1]} {selected_athlete[2]} checked in successfully with bib '{bib_stripped}'.")
        except Exception as e:
            st.error(f"Failed to check in athlete: {e}")

# Show checked-in athletes for selected event
st.subheader(f"Checked-In Athletes for {event_options[selected_event_index]}")
checked_in = conn.execute("""
    SELECT a.first_name, a.last_name, ac.bib_number, ac.checkin_time
    FROM athlete_checkins ac
    JOIN athletes a ON ac.athlete_id = a.id
    WHERE ac.event_id = ?
    ORDER BY ac.checkin_time
""", (selected_event_id,)).fetchall()

if checked_in:
    for first, last, bib, checkin_time in checked_in:
        bib_display = f" (Bib: {bib})" if bib else ""
        st.write(f"{first} {last}{bib_display} - checked in at {checkin_time}")
else:
    st.info("No athletes checked in for this event yet.")
