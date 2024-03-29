import streamlit as st
from dotenv import load_dotenv, set_key
import os
from main.cs_format import CSFormat

st.set_page_config(page_title="Code Server Format")

dirname = os.path.dirname(__file__)
dotenv_path = os.path.join(dirname, "../../.env")
# Load the environment variables from the .env file
def check_and_create_dotenv(dotenv_path):
    if not os.path.exists(dotenv_path):
        with open(dotenv_path, 'w') as f:
            pass  # Just create the file if it doesn't exist
# Before loading the .env file, check if it exists and create it if it doesn't
check_and_create_dotenv(dotenv_path)
password = ""
output_table_name = ""
# Load the environment variables from the .env file
load_dotenv(dotenv_path=dotenv_path)

def update_env_file(key, value):
    # Reuse the dotenv_path variable defined earlier
    set_key(dotenv_path, key, value)

def update_progress(progress):
    progress_bar.progress(progress)

# Streamlit UI
st.title('Code Server Format')
# Check if processing has been initialized
if 'processing_started' not in st.session_state:
    st.session_state.processing_started = False
if not st.session_state.processing_started:
    with st.form("config_form"):
        username = st.text_input("USERNAME", os.getenv("USERNAME"))
        password = st.text_input("PASSWORD", type="password")
        connection_address = st.text_input("CONNECTION_ADDRESS", os.getenv("CONNECTION_ADDRESS"))
        port = st.text_input("PORT", os.getenv("PORT"))
        database = st.text_input("DATABASE", os.getenv("DATABASE"))
        schema = st.text_input("SCHEMA", os.getenv("SCHEMA"))
        table = st.text_input("TABLE", os.getenv("TABLE"))
        output_table_name = st.text_input("OUTPUT_TABLE_NAME")
        submitted = st.form_submit_button("Update")
        if submitted:
            # Update other variables in the .env file
            update_env_file("USERNAME", username)
            update_env_file("CONNECTION_ADDRESS", connection_address)
            update_env_file("PORT", port)
            update_env_file("DATABASE", database)
            update_env_file("SCHEMA", schema)
            update_env_file("TABLE", table)
            st.session_state.processing_started = True
            st.rerun()
if st.session_state.processing_started:
    # Processing phase
    progress_bar = st.progress(0)
    # Initialize and run the processing logic
    main_process = CSFormat(password, output_table_name) # Ensure this uses updated environment variables if needed
    password = ""
    main_process.run(progress_callback=update_progress)
    progress_bar.empty()  # Clear the progress bar
    # Show download button
    dirname = os.path.dirname(__file__)
    processed_file_path = os.path.join(dirname, os.getenv('OUTPUT_FILE_PATH'), output_table_name)
    with open(processed_file_path, "rb") as file:
        st.download_button(
            label="Download Code Server Format Excel File",
            data=file,
            file_name=os.getenv('OUTPUT_FILE_NAME'),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    st.button("Reset", on_click=lambda: st.session_state.update(processing_started=False))