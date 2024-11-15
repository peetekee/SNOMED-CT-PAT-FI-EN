# SNOMED-CT-PAT-FI-EN
status: draft

This application is a tool for updating the SNOMED CT PAT FI database and converting the database table to Code Server format.
Only english language is supported. Language row updates are automated based on the english language row.

## Getting Started
1. Ensure that you have Python 3.8 or later installed.
2. Clone the repository and navigate to the project directory.
    ```bash
    git clone https://github.com/peetekee/SNOMED-CT-PAT-FI-EN.git
    cd SNOMED-CT-PAT-FI-EN
    ```
3. Create a virtual environment:
    ```bash
    python -m venv .venv
    ```
4. Activate the virtual environment:
    ```bash
    source .venv/bin/activate
    ```
5. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Run the application:
    ```bash
    invoke start
    ```
7. The application should now be running. You can access it by navigating to `http://localhost:5000` in your browser.

See the [technical design document](technical_design_document.md) for more information.
Paula Kujala is responsible for the documentation of the update process from the pathologist's point of view.
