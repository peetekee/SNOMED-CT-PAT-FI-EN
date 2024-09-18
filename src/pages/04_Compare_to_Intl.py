import streamlit as st
from dotenv import load_dotenv, set_key
import os
from main import CompareIntl

dirname = os.path.dirname(__file__)
dotenv_path = os.path.join(dirname, "../../.env")
logo_url = os.path.join(dirname, "assets/thl_logo_fi.png")

# Sidebar logo
st.sidebar.image(logo_url, use_column_width=True)

# Ensure .env file exists
def check_and_create_dotenv(dotenv_path):
    if not os.path.exists(dotenv_path):
        raise Exception("NO .ENV FILE")

check_and_create_dotenv(dotenv_path)
load_dotenv(dotenv_path=dotenv_path)

def update_env_file(key, value):
    # Reuse the dotenv_path variable defined earlier
    set_key(dotenv_path, key, value)

with st.form("config_form"):
    username = st.text_input("Username", os.getenv("USERNAME"))
    password = st.text_input("Password", type="password")
    connection_address = st.text_input(
        "Connection Address", os.getenv("CONNECTION_ADDRESS"))
    port = st.text_input("Port", os.getenv("PORT"))
    database = st.text_input("Database", os.getenv("DATABASE"))
    schema = st.text_input("sct_pat_fi Schema", os.getenv("SCHEMA"))
    table = st.text_input("sct_pat_fi Table", os.getenv("TABLE"))
    intl_schema = st.text_input("International Release Schema", os.getenv("INTL_SCHEMA"))
    submitted = st.form_submit_button("Update")
    if submitted:
        update_env_file("USERNAME", username)
        st.session_state.password = password
        update_env_file("CONNECTION_ADDRESS", connection_address)
        update_env_file("PORT", port)
        update_env_file("DATABASE", database)
        update_env_file("SCHEMA", schema)
        update_env_file("TABLE", table)
        update_env_file("INTL_SCHEMA", intl_schema)
        comp = CompareIntl(password)