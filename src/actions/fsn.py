import pandas as pd
from config import COLUMNS
from services.components import Get, Put


class FSN:
    """Change row FSN. This will affect all rows with the same concept.
    """

    def __init__(self, database: 'pd.DataFrame', fsn_edit_en_rows: 'pd.DataFrame'):
        self.__database = database
        self.__fsn_edit_en_rows = fsn_edit_en_rows

    def commit(self):
        for _, en_row in self.__fsn_edit_en_rows.iterrows():
            lang_rows = Get.lang_rows_by_en(
                self.__database, en_row)

            for _, lang_row in lang_rows.iterrows():
                index = Get.index_by_codeid(
                    self.__database, lang_row[COLUMNS["code_id"]])
                self.__database = Put.fsn(
                    self.__database, index, en_row[COLUMNS["concept_fsn"]], en_row[COLUMNS["edit_comment"]])
                
            index = Get.index_by_codeid(
                self.__database, en_row[COLUMNS["code_id"]])
            self.__database = Put.fsn(
                self.__database, index, en_row[COLUMNS["concept_fsn"]], en_row[COLUMNS["edit_comment"]])

        return self.__database
