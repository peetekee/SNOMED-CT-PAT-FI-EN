import streamlit as st
import os

dirname = os.path.dirname(__file__)

logo_url = os.path.join(dirname, "pages/assets/thl_logo_fi.png")

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

st.markdown(
    """
# Welcome to the Finnish SNOMED CT Pathology Database Management Portal

## Streamlining Pathology Updates for SCT PAT FI

### Introduction
This portal is designed to manage and update the Finnish SCT PAT FI database with pathology changes. It simplifies the process of integrating pathologist modifications, converting data into Code server format, performing technical checks, and managing related files efficiently.

### Core Functionalities
- **Database Updates**: Upload predefined Excel files to apply pathologist changes to the SNOMED CT PAT FI database.
- **Code Server Format Conversion**: Convert specific SCT PAT FI versions into a code server format.
- **Technical Checks**: Perform technical checks on specific SCT PAT FI versions to ensure integrity before deployment.
- **File Management**: A comprehensive system to download, and manage files related to SCT PAT FI updates.
    """
)
