import streamlit as st
import duckdb
from datetime import datetime

st.title("Split Logger")

conn = duckdb.connect("motherduck.duckdb")

# Hardcoded groups and splits
ATHLETE_GROUPS = {
    1: "Varsity",
    2: "Subvarsity",
    3: "JV"
}

SPLIT_LOCATIONS = {
    1: "0.5 mile",
    2: "1 mile",
    3: "2 mile",
    4: "2.6 mile",
    5: "Final"
}

# Select event
events = conn.execute("SELECT id, event_name, date FROM events ORDER BY date DESC").fetchall()
if not events:
    st.warning("No events found. Please add events on the Event Entry page.")
    st.stop()

event_options = [f"{name} ({date})" for _, name, date in events]
selected_event_idx = st.selectbox("Select Event", range(len(events)), format_func=lambda i: event_options[i])
selected_event_id = events[selected_event_idx][0]

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
        SELECT a.id, a.first_name, a.last_name,
            COALESCE(ac.bib_number, 'N/A') AS bib_number
        FROM athletes a
        LEFT JOIN athlete_checkins ac
            ON a.id = ac.athlete_id AND ac.event_id = ?
        WHERE a.group_id = ?
        ORDER BY a.last_name, a.first_name
    """
    return conn.execute(query, [selected_event_id, group_id]).fetchall()

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

st.write(f"### Event: {events[selected_event_idx][1]} ({events[selected_event_idx][2]})")
st.write(f"### Recording splits for: {SPLIT_LOCATIONS[selected_split_id]}")

for group_id, group_name in ATHLETE_GROUPS.items():
    st.write(f"#### {group_name}")
    athletes = get_athletes_by_group(group_id)
    if not athletes:
        st.write("No athletes found in this group.")
        continue

    cols = st.columns(4)
    for i, athlete in enumerate(athletes):
        athlete_id, first_name, last_name, bib_number = athlete
        label = f"{first_name} {last_name} (Bib: {bib_number})"
        if cols[i % 4].button(label, key=f"{group_id}_{athlete_id}"):
            current_time = datetime.now()
            split_seconds = (current_time - start_time).total_seconds()
            try:
                record_split(athlete_id, selected_split_id, split_seconds)
                st.success(f"Split recorded for {first_name} {last_name}: {split_seconds:.2f} sec")
            except Exception as e:
                st.error(f"Error recording split: {e}")
