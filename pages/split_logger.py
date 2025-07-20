import streamlit as st
import duckdb
from datetime import datetime

st.title("Split Logger")

conn = duckdb.connect("motherduck.duckdb")

# Hardcoded groups
ATHLETE_GROUPS = {
    1: "Varsity",
    2: "Subvarsity",
    3: "JV"
}

# Hardcoded split groups
SPLIT_GROUPS = {
    1: "0.5 mile",
    2: "1 mile",
    3: "2 mile",
    4: "2.6 mile",
    5: "Final"
}

# Select event
events = conn.execute("SELECT id, event_name, date FROM events ORDER BY date DESC").fetchall()
if not events:
    st.warning("No events found. Please add events first.")
    st.stop()

event_options = [f"{name} ({date})" for _, name, date in events]
selected_event_index = st.selectbox("Select Event", range(len(event_options)), format_func=lambda i: event_options[i])
selected_event_id = events[selected_event_index][0]

# Select split location
split_id = st.selectbox("Select Split Location", list(SPLIT_GROUPS.keys()), format_func=lambda i: SPLIT_GROUPS[i])

# Fetch athletes grouped by group_id, sorted by last_name, first_name
athletes = conn.execute("""
    SELECT a.id, a.first_name, a.last_name, a.group_id,
        ac.bib_number
    FROM athletes a
    LEFT JOIN athlete_checkins ac ON a.id = ac.athlete_id AND ac.event_id = ?
    ORDER BY a.group_id, a.last_name, a.first_name
""", (selected_event_id,)).fetchall()

# Organize athletes by group
grouped_athletes = {gid: [] for gid in ATHLETE_GROUPS.keys()}
for row in athletes:
    athlete_id, first_name, last_name, group_id, bib = row
    grouped_athletes[group_id].append({
        "id": athlete_id,
        "full_name": f"{first_name} {last_name}",
        "bib_number": bib if bib is not None else ""
    })

st.write("### Athlete Splits")

for group_id, group_name in ATHLETE_GROUPS.items():
    st.write(f"#### {group_name}")
    group_athletes = grouped_athletes.get(group_id, [])
    if not group_athletes:
        st.write("No athletes in this group.")
        continue

    # Build columns header
    cols = st.columns([3, 2, 2])
    cols[0].write("Athlete Name")
    cols[1].write("Bib Number")
    cols[2].write("Record Split")

    for athlete in group_athletes:
        cols = st.columns([3, 2, 2])
        cols[0].write(athlete["full_name"])
        cols[1].write(athlete["bib_number"])

        # Unique key for each button to avoid collisions
        button_key = f"split_{selected_event_id}_{split_id}_{athlete['id']}"

        if cols[2].button("Record Split", key=button_key):
            now = datetime.now().isoformat()
            try:
                conn.execute("""
                    INSERT INTO split_times (athlete_id, event_id, split_id, split_time)
                    VALUES (?, ?, ?, ?)
                """, (athlete["id"], selected_event_id, split_id, now))
                st.success(f"Recorded {SPLIT_GROUPS[split_id]} split for {athlete['full_name']}")
            except Exception as e:
                st.error(f"Error recording split for {athlete['full_name']}: {e}")
