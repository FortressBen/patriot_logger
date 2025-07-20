import streamlit as st
import duckdb

st.title("Admin Page")

# Connect to the DuckDB database
conn = duckdb.connect("motherduck.duckdb")

# Section 1: Create tables button
st.header("Initialize Database Tables")

if st.button("Create Tables"):
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS athlete_groups (
                id INTEGER,
                name TEXT
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS athletes (
                id INTEGER,
                first_name TEXT,
                last_name TEXT,
                group_id INTEGER,
                bib_number TEXT
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_name TEXT,
                date TEXT
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS split_ids (
                id INTEGER,
                name TEXT
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS split_times (
                athlete_id INTEGER,
                event_id INTEGER,
                split_id INTEGER,
                time_elapsed TEXT
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS athlete_checkins (
                athlete_id INTEGER,
                event_id INTEGER,
                checkin_time TEXT
            );
        """)
        st.success("Tables created successfully.")
    except Exception as e:
        st.error(f"Error creating tables: {e}")

# Section 2: SQL Execution Tool
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
