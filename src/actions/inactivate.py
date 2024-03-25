import pandas as pd
from config import COLUMNS
from services.components import Get, Put


class Inactivate:
    """Inactivates the en row and the associated lang rows

    Given a list of inactivated en rows, inactivates the en row and the associated lang rows in the database
    """

    def __init__(self, database: 'pd.DataFrame', inactivated_en_rows: 'pd.DataFrame', config: object) -> None:
        self.__database = database
        self.__inactivated_en_rows = inactivated_en_rows
        self.__config = config

    def __inactivate_rows(self, en_row: 'pd.Series'):
        """Inactivates the en row and the associated lang rows
        """

        lang_rows = Get.lang_rows_by_en(
            self.__database, en_row)

        for _, lang_row in lang_rows.iterrows():
            # Inactivate lang_row
            self.__database = Put.inactivate_row(
                lang_row[COLUMNS["code_id"]], self.__database, self.__config.version_date, en_row[COLUMNS["inaktivoinnin_selite"]], en_row[COLUMNS["edit_comment"]])

        # Inactivate en_row
        self.__database = Put.inactivate_row(
            en_row[COLUMNS["code_id"]], self.__database, self.__config.version_date, en_row[COLUMNS["inaktivoinnin_selite"]], en_row[COLUMNS["edit_comment"]])

    def commit(self):
        """Main function for inactivating rows
        """

        for _, en_row in self.__inactivated_en_rows.iterrows():
            self.__inactivate_rows(en_row)
        return self.__database
