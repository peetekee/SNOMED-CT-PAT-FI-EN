import pandas as pd
from .update import Update
from services import Excel
from config import Config


class UpdateIntl:
    def __init__(self, password) -> None:
        self.__password = password
        self.__conf = Config(password)
        self.__excel = Excel(self.__conf)

    def __get_accepted_intl_updates(self):
        intl_updates = self.__excel.get()
    
        # Separate old and new rows
        old_rows = intl_updates[intl_updates['status'].isna()]
        new_rows = intl_updates[(intl_updates['status'].isin(['new_concept', 'fsn'])) & (intl_updates['accept'] == 'x')]

        # Filter old rows to only include those with a matching CodeId in new_rows
        filtered_old_rows = old_rows[old_rows['CodeId'].isin(new_rows['CodeId'])]

        # Check for multiple accepted entries for the same CodeId
        multiple_accepted = new_rows.duplicated(subset=['CodeId'], keep=False)
        if multiple_accepted.any():
            print("Error: Multiple accepted suggestions for an old row.")
        else:
            # Concatenate the filtered old rows with new rows, and sort by CodeId
            return pd.concat([filtered_old_rows, new_rows]).sort_values(by='CodeId').reset_index(drop=True)
    
    def run(self, progress_callback=None):
        update_excel = self.__get_accepted_intl_updates()
        update_excel = update_excel.drop(columns=['accept', 'meta'])
        Update(password=self.__password, intl=True, table=update_excel).run(progress_callback=progress_callback)
