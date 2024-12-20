import streamlit as st
from dotenv import load_dotenv, set_key
import os
from main import Update, UpdateIntl

dirname = os.path.dirname(__file__)
dotenv_path = os.path.join(dirname, "../../.env")

logo_url = os.path.join(dirname, "assets/thl_logo_fi.png")

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


def check_and_create_dotenv(dotenv_path):
    if not os.path.exists(dotenv_path):
        with open(dotenv_path, 'w') as f:
            pass  # Just create the file if it doesn't exist


check_and_create_dotenv(dotenv_path)
load_dotenv(dotenv_path=dotenv_path)


def update_env_file(key, value):
    set_key(dotenv_path, key, value)


def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        save_path = os.path.join(dirname, os.getenv('UPLOAD_PATH'))
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        full_path = os.path.join(save_path, uploaded_file.name)
        with open(full_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return full_path
    return None


def update_progress(progress):
    progress_bar.progress(progress)


st.title('Update SNOMED CT PAT FI')

update_type = st.selectbox("Select Update Type", ["intl-update", "manual-update"])

if 'confirmation_pending' not in st.session_state:
    st.session_state.confirmation_pending = False
if 'update_processing_started' not in st.session_state:
    st.session_state.update_processing_started = False
if 'update_processing_completed' not in st.session_state:
    st.session_state.update_processing_completed = False

if not st.session_state.update_processing_started and not st.session_state.update_processing_completed:
    excel_file = st.file_uploader("EXCEL_FILE", type=['xlsx'])
    with st.form("config_form"):
        username = st.text_input("USERNAME", os.getenv("USERNAME"))
        password = st.text_input("PASSWORD", type="password")
        connection_address = st.text_input("CONNECTION_ADDRESS", os.getenv("CONNECTION_ADDRESS"))
        port = st.text_input("PORT", os.getenv("PORT"))
        database = st.text_input("DATABASE", os.getenv("DATABASE"))
        schema = st.text_input("SCHEMA", os.getenv("SCHEMA"))
        table = st.text_input("TABLE", os.getenv("TABLE"))
        excel_sheet = st.text_input("EXCEL_SHEET", os.getenv("EXCEL_SHEET"))
        output_file_name = st.text_input("OUTPUT_FILE_NAME")
        output_table = st.text_input("OUTPUT_TABLE", os.getenv("OUTPUT_TABLE"))
        date = st.text_input("DATE", os.getenv("DATE"))
        default_expiring_date = st.text_input("DEFAULT_EXPIRING_DATE", os.getenv("DEFAULT_EXPIRING_DATE"))
        submitted = st.form_submit_button("Update")
        
        if submitted:
            if excel_file is not None:
                file_path = save_uploaded_file(excel_file)
                if file_path:
                    update_env_file("EXCEL_FILE", file_path)
            update_env_file("USERNAME", username)
            st.session_state.password = password
            update_env_file("CONNECTION_ADDRESS", connection_address)
            update_env_file("PORT", port)
            update_env_file("DATABASE", database)
            update_env_file("SCHEMA", schema)
            update_env_file("TABLE", table)
            update_env_file("EXCEL_SHEET", excel_sheet)
            update_env_file("OUTPUT_FILE", os.path.join(dirname, os.getenv("DOWNLOAD_PATH"), output_file_name))
            update_env_file("OUTPUT_TABLE", output_table)
            update_env_file("DATE", date)
            update_env_file("DEFAULT_EXPIRING_DATE", default_expiring_date)

            # Trigger confirmation popup
            st.session_state.confirmation_pending = True

if st.session_state.confirmation_pending:
    st.warning(f"Are you sure you want to proceed with '{update_type}'?")
    confirm_button = st.button("Yes, proceed")
    cancel_button = st.button("Cancel")
    
    if confirm_button:
        st.session_state.confirmation_pending = False
        st.session_state.update_processing_started = True
        st.session_state.update_type = update_type
        st.experimental_rerun()
        
    elif cancel_button:
        st.session_state.confirmation_pending = False
        st.session_state.update_processing_started = False

if st.session_state.update_processing_started:
    load_dotenv(dotenv_path=dotenv_path, override=True)
    progress_bar = st.progress(0)

    if st.session_state.update_type == "intl-update":
        main_process = UpdateIntl(st.session_state.password)
    else:
        main_process = Update(st.session_state.password)

    st.session_state.password = None
    main_process.run(progress_callback=update_progress)
    progress_bar.empty()
    st.session_state.update(update_processing_completed=True, update_processing_started=False)

if st.session_state.update_processing_completed:
    processed_file_path = os.getenv("OUTPUT_FILE")
    with open(processed_file_path, "rb") as file:
        st.download_button(
            label="Download Processed Excel File",
            data=file,
            file_name=os.path.basename(os.getenv("OUTPUT_FILE")),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    st.button("Reset", on_click=lambda: st.session_state.update(update_processing_started=False, update_processing_completed=False, confirmation_pending=False))
