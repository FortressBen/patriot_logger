import streamlit as st
import duckdb
import pandas as pd

st.title("Athlete Upload")

conn = duckdb.connect("motherduck.duckdb")

# Hardcoded athlete groups dict (ID -> Name)
ATHLETE_GROUPS = {
    1: "Varsity",
    2: "Subvarsity",
    3: "JV"
}

# Show group selection for CSV upload - user must assign groups in CSV by ID or Name?
st.write("Athlete groups are hardcoded:")
for id_, name in ATHLETE_GROUPS.items():
    st.write(f"{id_}: {name}")

uploaded_file = st.file_uploader("Upload CSV file with columns: first_name, last_name, group_id (1=Varsity, 2=Subvarsity, 3=JV)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Validate required columns
        if not {"first_name", "last_name", "group_id"}.issubset(df.columns):
            st.error("CSV must contain columns: first_name, last_name, group_id")
        else:
            # Validate group_id values
            invalid_groups = set(df['group_id']) - set(ATHLETE_GROUPS.keys())
            if invalid_groups:
                st.error(f"Invalid group_id values in CSV: {invalid_groups}. Use 1, 2, or 3.")
            else:
                # Assign IDs to athletes
                max_id = conn.execute("SELECT MAX(id) FROM athletes").fetchone()[0]
                start_id = max_id + 1 if max_id is not None else 1
                df['id'] = range(start_id, start_id + len(df))

                # Reorder columns for insert (id, first_name, last_name, group_id)
                df = df[['id', 'first_name', 'last_name', 'group_id']]

                # Insert into DB
                conn.execute("BEGIN TRANSACTION")
                for _, row in df.iterrows():
                    conn.execute(
                        "INSERT INTO athletes (id, first_name, last_name, group_id) VALUES (?, ?, ?, ?)",
                        (int(row['id']), row['first_name'], row['last_name'], int(row['group_id']))
                    )
                conn.execute("COMMIT")

                st.success(f"Uploaded {len(df)} athletes successfully!")

    except Exception as e:
        st.error(f"Error uploading athletes: {e}")
