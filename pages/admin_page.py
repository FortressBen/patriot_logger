import streamlit as st
from page_components import make_header
from db import conn,create_tables, delete_tables

make_header("Administration")

if st.button("Create Database Tables"):
    try:
        delete_tables()
        create_tables()
        st.success("Tables created successfully in motherduck.duckdb.")
    except Exception as e:
        st.error(f"Error creating tables: {e}")

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