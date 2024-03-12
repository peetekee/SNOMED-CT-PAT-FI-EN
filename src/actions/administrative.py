import pandas as pd
from services.components import Put, Get
from config import COLUMNS


class Administrative:
    """Only update columns that are not in the koodistopalvelu
    """
    ADMINISTRATIVE_COLUMNS = [
        COLUMNS["tays_snomed_ii"],
        COLUMNS["parent_concept_id"],
        COLUMNS["parent_concept_fsn"],
        COLUMNS["edit_comment"],
        COLUMNS["av_notes"],
        COLUMNS["icdo_term"],
        COLUMNS["icdo_synonyms"],
        COLUMNS["sn2_code"],
        COLUMNS["sn2_term"],
        COLUMNS["endo"],
        COLUMNS["gastro"],
        COLUMNS["gyne"],
        COLUMNS["iho"],
        COLUMNS["hema"],
        COLUMNS["keuhko"],
        COLUMNS["nefro"],
        COLUMNS["neuro"],
        COLUMNS["paa_kaula"],
        COLUMNS["pedi"],
        COLUMNS["pehmyt"],
        COLUMNS["rinta"],
        COLUMNS["syto"],
        COLUMNS["uro"],
        COLUMNS["verenkierto_yleiset"],
    ]

    def __init__(self, database: 'pd.DataFrame', administrative_en_rows: 'pd.DataFrame'):
        self.__database = database
        self.__administrative_en_rows = administrative_en_rows

    def __update_administrative_columns(self, en_row: 'pd.Series'):
        lang_rows = Get.lang_rows_by_en(
            self.__database, en_row)

        for _, lang_row in lang_rows.iterrows():
            index = Get.index_by_codeid(
                self.__database, lang_row[COLUMNS["code_id"]])
            self.__database = Put.administrative_columns(
                self.__database, index, en_row, self.ADMINISTRATIVE_COLUMNS)

        index = Get.index_by_codeid(
            self.__database, en_row[COLUMNS["code_id"]])
        self.__database = Put.administrative_columns(
            self.__database, index, en_row, self.ADMINISTRATIVE_COLUMNS)

    def commit(self):
        for _, en_row in self.__administrative_en_rows.iterrows():
            self.__update_administrative_columns(en_row)
        return self.__database
