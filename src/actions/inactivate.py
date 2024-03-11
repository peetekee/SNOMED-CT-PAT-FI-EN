import pandas as pd
from config import COLUMNS, Config
from services.components import Get, Put


class Inactivate:
    """Inactivates the en row and the associated lang rows

    Given a list of inactivated en rows, inactivates the en row and the associated lang rows in the database
    """

    def __init__(self, database: 'pd.DataFrame', inactivated_en_rows: 'pd.DataFrame'):
        self.__database = database
        self.__inactivated_en_rows = inactivated_en_rows
        self.__config = Config()

    def commit(self):
        for _, en_row in self.__inactivated_en_rows.iterrows():
            # Get associated lang rows
            lang_rows = Get.lang_rows_by_en(
                self.__database, en_row)

            for _, lang_row in lang_rows.iterrows():
                # Inactivate lang_row
                index = Get.index_by_codeid(
                    self.__database, lang_row[COLUMNS["code_id"]])
                self.__database = Put.inactivated_row(
                    self.__database, index, self.__config.version_date, en_row[COLUMNS["inaktivoinnin_selite"]], en_row[COLUMNS["edit_comment"]])

            # Inactivate en_row
            index = Get.index_by_codeid(
                self.__database, en_row[COLUMNS["code_id"]])
            self.__database = Put.inactivated_row(
                self.__database, index, self.__config.version_date, en_row[COLUMNS["inaktivoinnin_selite"]], en_row[COLUMNS["edit_comment"]])

        return self.__database
