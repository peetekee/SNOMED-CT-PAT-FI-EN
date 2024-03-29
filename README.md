# SNOMED-CT-PAT-FI-EN
status: draft

This application is a tool for updating the SNOMED CT PAT FI database and converting the database table to Code Server format.
Only english language is supported. Language row updates are automated based on the english language row.

## Getting Started
1. Ensure that you have Python 3.8 or later installed.
2. Install poetry by running:
    ```bash
    pip install poetry
    ```
3. Clone the repository and navigate to the project directory.
    ```bash
    git clone https://github.com/peetekee/SNOMED-CT-PAT-FI-EN.git
4. Install the dependencies by running:
    ```bash
    poetry install
    ```
5. Run the application by running:
    ```bash
    poetry run invoke start
    ```

See the [technical design document](technical_design_document.md) for more information.
Paula Kujala is responsible for the documentation of the update process from the pathologist's point of view.
