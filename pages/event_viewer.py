import streamlit as st
import duckdb
import datetime
import time

st.title("Event Viewer and Race Clock")

conn = duckdb.connect("motherduck.duckdb")

# Create events table if not exists
conn.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    event_name TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

# Fetch events sorted by date descending
events = conn.execute("SELECT id, event_name, date FROM events ORDER BY date DESC").fetchall()
if not events:
    st.info("No events found. Please add events on the Event Entry page.")
    st.stop()

# Prepare dropdown with event display names
event_options = [f"{name} ({date})" for _, name, date in events]
event_ids = [eid for eid, _, _ in events]

selected_index = st.selectbox("Select Event", options=range(len(event_options)), format_func=lambda i: event_options[i])
selected_event_id = event_ids[selected_index]

# Save selected event id in session state so split_logger can access it
st.session_state.selected_event_id = selected_event_id

# Initialize the race clock start times dictionary in session_state if not present
if 'race_clock_start_times' not in st.session_state:
    st.session_state.race_clock_start_times = {}

# Buttons for starting and stopping the race clock
col1, col2 = st.columns(2)

with col1:
    if st.button("Start Race Clock"):
        st.session_state.race_clock_start_times[selected_event_id] = datetime.datetime.now()
        st.success("Race clock started!")

with col2:
    if st.button("Stop Race Clock"):
        if selected_event_id in st.session_state.race_clock_start_times:
            del st.session_state.race_clock_start_times[selected_event_id]
            st.success("Race clock stopped!")
        else:
            st.warning("Race clock is not running.")

# Display live race timer if started
if selected_event_id in st.session_state.race_clock_start_times:
    start_time = st.session_state.race_clock_start_times[selected_event_id]
    # Calculate elapsed time
    elapsed = datetime.datetime.now() - start_time
    # Display as hh:mm:ss
    st.markdown(f"**Race Clock Running:** {str(elapsed).split('.')[0]}")
else:
    st.markdown("**Race Clock is stopped.**")

# Show which athletes are checked in to this event
st.header("Checked-In Athletes")

checked_in_athletes = conn.execute("""
    SELECT a.first_name, a.last_name, ac.checkin_time
    FROM athlete_checkins ac
    JOIN athletes a ON ac.athlete_id = a.id
    WHERE ac.event_id = ?
    ORDER BY a.last_name, a.first_name
""", (selected_event_id,)).fetchall()

if checked_in_athletes:
    for first_name, last_name, checkin_time in checked_in_athletes:
        st.write(f"{first_name} {last_name} (Checked in at {checkin_time})")
else:
    st.write("No athletes checked in for this event yet.")
