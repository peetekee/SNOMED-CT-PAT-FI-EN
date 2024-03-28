import pandas as pd
from config import COLUMNS, Config
from services.components import Get, Put


class Activate:
    """Class for activating rows

    This class is used to activate rows in the database.
    It takes the database and the rows to be activated as input and activates the rows in the database.

    Currently, not much in use.
    """

    def __init__(self, database: 'pd.DataFrame', activated_en_rows: 'pd.DataFrame'):
        self.__database = database
        self.__activated_en_rows = activated_en_rows
        self.__config = Config()

    def __activate_rows(self, en_row: 'pd.Series'):
        """Activates the rows in the database

        Takes in the en rown and activates all the rows in the database that are related to the en row
        by en_row_code_id.

        Args:
            en_row (pd.Series): The rows to be activated
        """

        lang_rows = Get.lang_rows_by_en(
            self.__database, en_row)

        for _, lang_row in lang_rows.iterrows():
            self.__database = Put.activate_row_row(
                lang_row[COLUMNS["code_id"]], self.__database, self.__config.version_date, self.__config.default_expiring_date, en_row[COLUMNS["inaktivoinnin_selite"]], en_row[COLUMNS["edit_comment"]])

        self.__database = Put.activate_row(
            en_row[COLUMNS["code_id"]], self.__database, self.__config.version_date, self.__config.default_expiring_date, en_row[COLUMNS["edit_comment"]])

    def commit(self):
        """Main function for activating rows
        """

        for _, en_row in self.__activated_en_rows.iterrows():
            self.__activate_rows(en_row)
        return self.__database
