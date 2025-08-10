import streamlit as st
from db import conn,get_athlete_groups,get_split_locations
from datetime import datetime
from page_components import make_header
make_header("Split Logger")

ATHLETE_GROUPS = get_athlete_groups()
SPLIT_LOCATIONS= get_split_locations().set_index('id')['split_name'].to_dict()

# Select event
events = conn.execute("SELECT id, event_name, date FROM events ORDER BY date").fetchall()
if not events:
    st.warning("No events found. Please add events on the Event Entry page.")
    st.stop()

event_options = [f"{name} ({date})" for _, name, date in events]
selected_event_idx = st.selectbox("Select Event", range(len(events)), format_func=lambda i: event_options[i])
selected_event_id = events[selected_event_idx][0]

# Select Recorder
recorders = conn.execute("SELECT DISTINCT recorder_nickname FROM athletes ORDER BY recorder_nickname").df()
recorders = (list(recorders['recorder_nickname']))

if len(recorders) == 0:
    st.warning("Load Some Athletes First.")
    st.stop()

recorder_options = [f"{recorder_nickname}" for recorder_nickname in recorders]
selected_recorder_idx = st.selectbox("Select Recorder Name", range(len(recorders)), format_func=lambda i: recorder_options[i])
selected_recorder_id = recorders[selected_recorder_idx]

# Select split location (pills style)
selected_split_id = st.radio(
    "Select Split Location",
    options=list(SPLIT_LOCATIONS.keys()),
    format_func=lambda k: SPLIT_LOCATIONS[k],
    horizontal=True
)

# Retrieve race clock start time for the selected event
start_time_raw = st.session_state.get("race_clock_start_times", {}).get(selected_event_id)
if start_time_raw and isinstance(start_time_raw, str):
    start_time = datetime.fromisoformat(start_time_raw)
else:
    start_time = start_time_raw

if start_time is None:
    st.error("Race clock for this event has not been started yet. Please start the clock on the Event Viewer page.")
    st.stop()

def get_athletes_by_group(group_id):
    query = """
        SELECT a.id, a.nickname,
                COALESCE(CAST(ac.bib_number AS TEXT), 'N/A') AS bib_number
        FROM athletes a
        LEFT JOIN athlete_checkins ac
            ON a.id = ac.athlete_id AND ac.event_id = ?
        WHERE a.group_id = ? AND a.recorder_nickname = ?
        ORDER BY a.nickname
    """
    return conn.execute(query, [selected_event_id, group_id, selected_recorder_id]).fetchall()

def record_split(athlete_id, split_id, split_seconds):
    existing = conn.execute(
        "SELECT split_time FROM split_times WHERE athlete_id = ? AND event_id = ? AND split_id = ?",
        [athlete_id, selected_event_id, split_id]
    ).fetchone()

    if existing:
        conn.execute(
            "UPDATE split_times SET split_time = ? WHERE athlete_id = ? AND event_id = ? AND split_id = ?",
            [split_seconds, athlete_id, selected_event_id, split_id]
        )
    else:
        conn.execute(
            "INSERT INTO split_times (athlete_id, event_id, split_id, split_time) VALUES (?, ?, ?, ?)",
            [athlete_id, selected_event_id, split_id, split_seconds]
        )

st.write(f"### Recording splits for: {SPLIT_LOCATIONS[selected_split_id]}")

for group_id, group_name in ATHLETE_GROUPS.items():
    st.write(f"#### {group_name}")
    athletes = get_athletes_by_group(group_id)
    if not athletes:
        st.write("No athletes found in this group.")
        continue

    cols = st.columns(4)
    for i, athlete in enumerate(athletes):
        athlete_id, nickname, bib_number = athlete
        label = f"{nickname} (Bib: {bib_number})"
        if cols[i % 4].button(label, key=f"{group_id}_{athlete_id}"):
            current_time = datetime.now()
            split_seconds = (current_time - start_time).total_seconds()
            try:
                record_split(athlete_id, selected_split_id, split_seconds)
                st.success(f"Split recorded for {nickname}: {split_seconds:.2f} sec")
            except Exception as e:
                st.error(f"Error recording split: {e}")
