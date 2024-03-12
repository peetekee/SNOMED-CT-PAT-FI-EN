import pandas as pd
from config import COLUMNS, Config
from services.components import Get, Put


class Activate:
    def __init__(self, database: 'pd.DataFrame', activated_en_rows: 'pd.DataFrame'):
        self.__database = database
        self.__activated_en_rows = activated_en_rows
        self.__config = Config()

    def __activate_rows(self, en_row: 'pd.Series'):
        lang_rows = Get.lang_rows_by_en(
            self.__database, en_row)

        for _, lang_row in lang_rows.iterrows():
            index = Get.index_by_codeid(
                self.__database, lang_row[COLUMNS["code_id"]])
            self.__database = Put.inactivated_row(
                self.__database, index, self.__config.version_date, self.__config.default_expiring_date, en_row[COLUMNS["inaktivoinnin_selite"]], en_row[COLUMNS["edit_comment"]])

        index = Get.index_by_codeid(
            self.__database, en_row[COLUMNS["code_id"]])
        self.__database = Put.inactivated_row(
            self.__database, index, self.__config.version_date, self.__config.default_expiring_date, en_row[COLUMNS["edit_comment"]])

    def commit(self):
        for _, en_row in self.__activated_en_rows.iterrows():
            self.__activate_rows(en_row)
        return self.__database
