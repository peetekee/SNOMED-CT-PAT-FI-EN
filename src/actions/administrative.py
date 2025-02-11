import pandas as pd
from services.components import Put, Get
from config import COLUMNS, ADMINISTRATIVE_COLUMNS


class Administrative:
    """Only update columns that are not in the koodistopalvelu

    This class is used to update the administrative columns in the database.
    It takes the database and the administrative rows as input and updates the administrative columns in the database.

    The administrative columns are the columns that are not in the koodistopalvelu.
    The columns are for internal use and are not visible to the end-users.
    """

    def __init__(self, database: 'pd.DataFrame', administrative_en_rows: 'pd.DataFrame'):
        self.__database = database
        self.__administrative_en_rows = administrative_en_rows

    def __update_administrative_columns(self, en_row: 'pd.Series'):
        """Updates the administrative columns of en and lang rows in the database
        """

        lang_rows = Get.lang_rows_by_en(
            self.__database, en_row)

        for _, lang_row in lang_rows.iterrows():
            self.__database = Put.administrative_columns(
                lang_row[COLUMNS["code_id"]], self.__database, en_row, ADMINISTRATIVE_COLUMNS)

        self.__database = Put.administrative_columns(
            en_row[COLUMNS["code_id"]], self.__database, en_row, ADMINISTRATIVE_COLUMNS)

    def commit(self):
        """Main function
        """

        for _, en_row in self.__administrative_en_rows.iterrows():
            self.__update_administrative_columns(en_row)
        return self.__database
