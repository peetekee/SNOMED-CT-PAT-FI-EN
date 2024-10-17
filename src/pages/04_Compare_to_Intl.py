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

def update_progress(progress):
    progress_bar.progress(progress)

# Streamlit UI
st.title('Compare to International Release')
# Check if processing has been initialized
if 'update_processing_started' not in st.session_state:
    st.session_state.update_processing_started = False
if 'update_processing_completed' not in st.session_state:
    st.session_state.update_processing_completed = False

if not st.session_state.update_processing_started and not st.session_state.update_processing_completed:
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
        output_file_name = st.text_input("Output file name")
        start = st.text_input("View Updates Between: start", os.getenv("VIEW_UPDATES_START"))
        end = st.text_input("View Updates Between: end", os.getenv("VIEW_UPDATES_END"))
        submitted = st.form_submit_button("Compare")
        if submitted:
            update_env_file("USERNAME", username)
            st.session_state.password = password
            update_env_file("CONNECTION_ADDRESS", connection_address)
            update_env_file("PORT", port)
            update_env_file("DATABASE", database)
            update_env_file("SCHEMA", schema)
            update_env_file("TABLE", table)
            update_env_file("INTL_OUTPUT_FILE", os.path.join(dirname, os.getenv("DOWNLOAD_PATH"), output_file_name))
            update_env_file("INTL_SCHEMA", intl_schema)
            update_env_file("VIEW_UPDATES_START", start)     
            update_env_file("VIEW_UPDATES_END", end)     
            st.session_state.start = start
            st.session_state.end = end
            comp = CompareIntl(password, start, end)
            st.session_state.update_processing_started = True
            st.rerun()
if st.session_state.update_processing_started:
    load_dotenv(dotenv_path=dotenv_path, override=True)
    # Processing phase
    progress_bar = st.progress(0)
    # Initialize and run the processing logic
    # Ensure this uses updated environment variables if needed
    main_process = CompareIntl(st.session_state.password, st.session_state.start, st.session_state.end)
    st.session_state.password = None  # Clear the password from the session state
    main_process.run(progress_callback=update_progress)
    progress_bar.empty()  # Clear the progress bar
    st.session_state.update(update_processing_completed=True, update_processing_started=False)

if st.session_state.update_processing_completed:
    # Show download button
    processed_file_path = os.getenv("INTL_OUTPUT_FILE")
    with open(processed_file_path, "rb") as file:
        st.download_button(
            label="Download Comparison Excel File",
            data=file,
            file_name=os.path.basename(os.getenv("INTL_OUTPUT_FILE")),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    st.button("Reset", on_click=lambda: st.session_state.update(update_processing_started=False, update_processing_completed=False))

