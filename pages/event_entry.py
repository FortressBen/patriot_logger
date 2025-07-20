import streamlit as st
import duckdb
from datetime import date

st.title("Event Entry")

conn = duckdb.connect("motherduck.duckdb")

# Create events and athlete_checkins tables if not exist
conn.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    event_name TEXT,
    date TEXT
)
""")
conn.execute("""
CREATE TABLE IF NOT EXISTS athlete_checkins (
    athlete_id INTEGER,
    event_id INTEGER,
    checkin_time TEXT
)
""")
conn.execute("""
CREATE TABLE IF NOT EXISTS athletes (
    id INTEGER,
    first_name TEXT,
    last_name TEXT,
    group_id INTEGER,
    bib_number TEXT
)
""")

# Add a new event form
with st.form("add_event_form"):
    event_name = st.text_input("Event Name")
    event_date = st.date_input("Event Date", value=date.today())
    submitted = st.form_submit_button("Add Event")

    if submitted:
        if event_name.strip() == "":
            st.error("Event name cannot be empty.")
        else:
            # Generate a new event ID manually
            max_id = conn.execute("SELECT MAX(id) FROM events").fetchone()[0]
            new_id = (max_id + 1) if max_id is not None else 1
            try:
                conn.execute(
                    "INSERT INTO events (id, event_name, date) VALUES (?, ?, ?)",
                    (new_id, event_name, event_date.isoformat())
                )
                st.success(f"Event '{event_name}' added successfully with ID {new_id}!")
            except Exception as e:
                st.error(f"Error adding event: {e}")

# Select event to view checked-in athletes
st.subheader("View Checked-in Athletes")

events = conn.execute("SELECT id, event_name, date FROM events ORDER BY date DESC").fetchall()
if events:
    event_options = [f"{name} ({date})" for _, name, date in events]
    selected_index = st.selectbox("Select Event", range(len(event_options)), format_func=lambda i: event_options[i])
    selected_event_id = events[selected_index][0]

    checked_in_df = conn.execute("""
        SELECT a.first_name, a.last_name, ac.bib_number, ac.checkin_time
        FROM athlete_checkins ac
        JOIN athletes a ON ac.athlete_id = a.id
        WHERE ac.event_id = ?
        ORDER BY ac.checkin_time
    """, (selected_event_id,)).df()

    if not checked_in_df.empty:
        st.dataframe(checked_in_df)
    else:
        st.info("No athletes have checked in for this event yet.")
else:
    st.info("No events found. Please add some events.")
