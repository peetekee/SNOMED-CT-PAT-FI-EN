import streamlit as st
import os

st.set_page_config(page_title="Checks")

dirname = os.path.dirname(__file__)
dotenv_path = os.path.join(dirname, "../../.env")

logo_url = os.path.join(dirname, "assets/thl_logo_fi.png")

st.sidebar.image(logo_url, use_column_width=True)

st.write(
    """TODO: will include the funtinality to run tests on the database table"""
)