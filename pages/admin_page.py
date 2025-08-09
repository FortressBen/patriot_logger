import streamlit as st
import duckdb
from pages.account import get_roles
from streamlit import session_state as ss
from auth import check_logged_in,AUTH_STATUS_KEY,get_role_for_user

check_logged_in()

st.title("Admin Page")
st.write("Administrative tools for database and configuration.")
user_role = get_role_for_user(ss.username)

conn = duckdb.connect("motherduck.duckdb")

create_tables_sql = """
CREATE TABLE IF NOT EXISTS athlete_groups (
    id INTEGER,
    group_name TEXT
);

DELETE FROM athlete_groups;
INSERT INTO athlete_groups (id,group_name)
VALUES
(1,'Varsity'),
(2,'Subvarsity'),
(3,'JV'),
(4,'Adults/Coaches');

CREATE TABLE IF NOT EXISTS athletes (
    id INTEGER,
    nickname TEXT,
    group_id INTEGER,
    recorder_nickname TEXT
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER,
    event_name TEXT,
    date TEXT
);

CREATE TABLE IF NOT EXISTS split_ids (
    id INTEGER,
    split_name TEXT
);

DELETE FROM split_ids;
INSERT INTO split_ids (id, split_name)
VALUES
(1,'0.5 Mile'),
(2,'1 Mile'),
(3,'2 Mile'),
(4,'2.6 Mile'),
(5,'Final');

CREATE TABLE IF NOT EXISTS split_times (
    id INTEGER,
    athlete_id INTEGER,
    event_id INTEGER,
    split_id INTEGER,
    split_time DOUBLE
);

CREATE TABLE IF NOT EXISTS athlete_checkins (
    id INTEGER,
    athlete_id INTEGER,
    event_id INTEGER,
    checkin_time TEXT,
    bib_number INTEGER
);
"""

if user_role == 'admin':
    if st.button("Create Database Tables"):
        try:
            conn.execute(create_tables_sql)
            st.success("Tables created successfully in motherduck.duckdb.")
        except Exception as e:
            st.error(f"Error creating tables: {e}")
else:
    st.write("No create tables for you.")

st.header("Run Custom SQL")

sql_input = st.text_area("Enter SQL statement", height=200)

if st.button("Run SQL"):
    if not sql_input.strip():
        st.warning("Please enter a SQL statement.")
    else:
        try:
            result = conn.execute(sql_input)

            if result.description:
                df = result.df()
                st.success("Query executed successfully.")
                st.dataframe(df)
            else:
                st.success("Statement executed successfully. No data returned.")
        except Exception as e:
            st.error(f"Error executing SQL: {e}")