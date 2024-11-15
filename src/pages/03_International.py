import streamlit as st
import subprocess
from dotenv import load_dotenv
import os
from services import Database
from config import Config

# Load the environment file path and logo
dirname = os.path.dirname(__file__)
dotenv_path = os.path.join(dirname, "../../.env")
logo_url = os.path.join(dirname, "assets/thl_logo_fi.png")

# Sidebar logo
st.sidebar.image(logo_url, use_column_width=True)
st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)

# Ensure .env file exists
def check_and_create_dotenv(dotenv_path):
    if not os.path.exists(dotenv_path):
        raise Exception("NO .ENV FILE")

check_and_create_dotenv(dotenv_path)
load_dotenv(dotenv_path=dotenv_path)

# Save uploaded zip file
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        save_path = os.path.join(dirname, os.getenv('INTL_ZIP_UPLOAD_PATH'))
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        full_path = os.path.join(save_path, uploaded_file.name)
        with open(full_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return full_path
    return None

# Function to run the bash command and stream the output in real-time
def run_command(file_path):
    script_path = os.path.join(dirname, "../intl/PostgreSQL/load_release-postgresql.sh")
    connection_address = os.getenv('CONNECTION_ADDRESS')
    database = os.getenv('DATABASE')
    load_type = "FULL"
    
    process = subprocess.Popen(
        [script_path, file_path, database, load_type, connection_address, st.session_state.password],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1  # Line-buffered for real-time output
    )

    # stdin when subprocess requests
    process.stdin.write(os.getenv('USERNAME') + "\n")
    process.stdin.write(os.getenv('PORT') + "\n")
    process.stdin.write("A" + "\n")

    for stdout_line in iter(process.stdout.readline, ""):
        st.text(stdout_line)
 
    # Stream the output line by line in real-time
    for stdout_line in iter(process.stderr.readline, ""):
        st.text(stdout_line)

# Main application
zip_file = st.file_uploader("International release zip", type=['zip'])
password = st.text_input("Password", type="password")

# When the form is submitted, upload the zip and run the command
if st.button("Upload to Database"):
    if zip_file is not None:
        # Save the uploaded file and get its path
        zip_path = save_uploaded_file(zip_file)
        if zip_path:
            st.session_state.password = password
            st.write(f"File uploaded: {zip_path}")
            # Run the bash script with the uploaded zip path
            run_command(zip_path)
            config = Config(st.session_state.password)
            st.session_state.password = ""
            db = Database(config)
            db.create_intl_views()
        else:
            st.error("File upload failed!")
    else:
        st.warning("Please upload a zip file.")
