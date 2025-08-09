import streamlit as st
from db import conn,get_athlete_groups
import pandas as pd
from page_components import make_header

make_header("Athlete Upload")

# Show group selection for CSV upload - user must assign groups in CSV by ID or Name?
st.write("Athlete groups are hardcoded:")
athlete_groups = get_athlete_groups()
valid_group_ids = athlete_groups['id'].to_list()
st.dataframe( athlete_groups,hide_index=True,width=200,)

uploaded_file = st.file_uploader("Upload CSV file with columns: nickname, recorder_nickname, group_id (1=Varsity, 2=Subvarsity, 3=JV, 4=Adults/Coaches)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Validate required columns
        if not {"nickname", "recorder_nickname", "group_id"}.issubset(df.columns):
            st.error("CSV must contain columns: nickname, recorder_nickname, group_id")
        else:
            # Validate group_id values
            invalid_groups = set(df['group_id']) - set(valid_group_ids)
            if invalid_groups:
                st.error(f"Invalid group_id values in CSV: {invalid_groups}. Use 1, 2, 3, or 4.")
            else:
                if st.button("Upload Athletes"):
                    # Assign IDs to athletes
                    max_id = conn.execute("SELECT MAX(id) FROM athletes").fetchone()[0]
                    start_id = max_id + 1 if max_id is not None else 1
                    df['id'] = range(start_id, start_id + len(df))

                    df = df[['id', 'nickname', 'recorder_nickname', 'group_id']]

                    conn.execute(
                        "DELETE FROM athletes",
                    )

                    # Insert into DB
                    conn.execute("BEGIN TRANSACTION")
                    for _, row in df.iterrows():
                        conn.execute(
                            "INSERT INTO athletes (id, nickname, recorder_nickname, group_id) VALUES (?, ?, ?, ?)",
                            (int(row['id']), row['nickname'], row['recorder_nickname'], int(row['group_id']))
                        )
                    conn.execute("COMMIT")

                    st.success(f"Uploaded {len(df)} athletes successfully!")

    except Exception as e:
        st.error(f"Error uploading athletes: {e}")