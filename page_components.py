import streamlit as st
from login import check_logged_in,ADMIN_ROLE
ALL_PAGES = {
    "home.py": "Home",
    "pages/admin_page.py": "Administration",
    "pages/athlete_check_in.py": "Athlete Check In",
    "pages/athlete_upload.py": "Upload Athletes",
    "pages/data_dump.py": "Data Dump",
    "pages/event_entry.py": "Event Entry",
    "pages/event_export.py": "Event Export",
    "pages/event_viewer.py": "Event Status",
    "pages/split_groups_entry.py": "Split Group Entry" ,
    "pages/split_logger.py": "Log Splits",
    "pages/logout.py": "Log Out"
}
ALL_PAGE_KEYS=list(ALL_PAGES.keys())

PAGES_BY_ROLE = {
    "admin": ALL_PAGE_KEYS,
    "student": ["home.py", "pages/split_logger.py", "pages/event_viewer.py","pages/logout.py"],
}

def make_nav():
    user_role = check_logged_in()
    with st.container(border=2,horizontal=True,horizontal_alignment="center"):
         for p in PAGES_BY_ROLE[user_role]:
            st.page_link(p, label=ALL_PAGES[p])
    st.divider(width="stretch")

def make_header(title: str):
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("static/jlmannlogo21.png", width=100)
    with col2:
        st.title(title)
    make_nav()