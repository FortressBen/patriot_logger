import streamlit as st
import duckdb
from app_secrets import SETTINGS

LOCAL_MODE = SETTINGS["LOCAL_DB"]
#ACCESS_TOKEN=st.secrets.get('motherduck',{}).get('token',None)
ACCESS_TOKEN = SETTINGS["ACCESS_TOKEN"]

MOTHERDUCK_DB_NAME = "patriot_logger"
LOCAL_DUCKDB_NAME = "mann_xc.duckdb"

if LOCAL_MODE:
    print("Using Local Mode Database")
    conn = duckdb.connect(LOCAL_DUCKDB_NAME)
else:
    print("Connecting to Motherduck Database")
    conn = duckdb.connect(f"md:{MOTHERDUCK_DB_NAME}?motherduck_token={ACCESS_TOKEN}")

def get_athlete_groups():
    return conn.execute("select id, group_name from athlete_groups").df()

def get_split_locations():
    return conn.execute("select id, split_name from split_ids").df()

def delete_tables():
    conn.execute("""
    DROP TABLE IF EXISTS athlete_groups;
    DROP TABLE IF EXISTS athletes;
    DROP TABLE IF EXISTS events;
    DROP TABLE IF EXISTS split_ids;
    DROP TABLE IF EXISTS split_times;
    DROP TABLE IF EXISTS athlete_checkins
    """)

def create_tables():

    conn.execute( """
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
        date TEXT,
        start_time TIMESTAMP,
        end_time TIMESTAMP
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
    """)



