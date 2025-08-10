import streamlit as st
from db import conn
import datetime
from login import get_user_role,ADMIN_ROLE
from page_components import make_header
make_header("Split Logger")


user_role = get_user_role()

# Fetch events sorted by date descending
events = conn.execute("SELECT id, event_name, date FROM events ORDER BY date").fetchall()
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
col1, col2, col3 = st.columns(3)

current_start_time, current_end_time = conn.execute("""
    select start_time, end_time from events where id = ?
""",[selected_event_id]).fetchone()


if user_role  == ADMIN_ROLE:
    with col1:
        if current_start_time is None and current_end_time is None:
            if st.button("Start Race Clock"):
                #st.session_state.race_clock_start_times[selected_event_id] = datetime.datetime.now()
                conn.execute("""
                        UPDATE events
                        SET start_time = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, [selected_event_id])
                st.success("Race clock started!")

    with col2:
        if current_start_time is not None and current_end_time is None:
            if st.button("Stop Race Clock"):
                #del st.session_state.race_clock_start_times[selected_event_id]
                conn.execute("""
                        UPDATE events
                        SET end_time = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, [selected_event_id])
                st.success("Race clock stopped!")

    with col3:
        if st.button("Reset Clocks"):
            conn.execute("""
                UPDATE events
                SET start_time = NULL, end_time = NULL
                WHERE id = ?
            """, [selected_event_id])
            st.success("Race clocks reset!")

# Display live race timer if started
if current_start_time is not None and current_end_time is None:
    elapsed = datetime.datetime.now() - current_start_time
    st.markdown(f"**Race Clock Running:** {str(elapsed).split('.')[0]}")
else:
    st.markdown("**Race Clock is stopped.**")

# Show which athletes are checked in to this event
st.header("Checked-In Athletes")

checked_in_athletes = conn.execute("""
    SELECT a.nickname, ac.checkin_time
    FROM athlete_checkins ac
    JOIN athletes a ON ac.athlete_id = a.id
    WHERE ac.event_id = ?
    ORDER BY a.nickname
""", (selected_event_id,)).fetchall()

if checked_in_athletes:
    for nickname, checkin_time in checked_in_athletes:
        st.write(f"{nickname} (Checked in at {checkin_time})")
else:
    st.write("No athletes checked in for this event yet.")
