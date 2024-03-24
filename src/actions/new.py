import pandas as pd
from config import COLUMNS, Config
from services.components import Get
from services.general import Verhoeff


class New:
    """Legacy is is the master
    """

    def __init__(self, database: 'pd.DataFrame', new_en_rows: 'pd.DataFrame'):
        self.__database = database
        self.__new_en_rows = new_en_rows
        self.__verhoeff = Verhoeff()
        self.__config = Config()

    def __set_code_id(self, en_row: 'pd.Series'):
        en_row[COLUMNS["code_id"]] = Get.next_codeid(self.__database)
        en_row[COLUMNS["en_row_code_id"]] = en_row[COLUMNS["code_id"]]
        return en_row

    def __set_concept_id(self, en_row: 'pd.Series'):
        concept_sn2, concept_sct = Get.legacyid(
            en_row[COLUMNS["legacy_concept_id"]])
        if concept_sn2 == None:
            raise Exception(
                "One of the new rows has missing or invalid legacy conceptid SN2 part")
        if concept_sct == None:
            concept_integer = Get.next_fin_extension_id(
                self.__database, COLUMNS["legacy_concept_id"])
            concept_sct = self.__verhoeff.generateVerhoeff(
                concept_integer, "10")

        en_row[COLUMNS["legacy_concept_id"]] = f"{concept_sn2}-{concept_sct}"
        en_row[COLUMNS["concept_id"]] = concept_sct
        return en_row

    def __set_term_id(self, en_row: 'pd.Series'):
        term_sn2, term_sct = Get.legacyid(en_row[COLUMNS["legacy_term_id"]])
        if term_sn2 == None:
            raise Exception(
                "One of the new rows has missing or invalid legacy termid SN2 part")
        if term_sct == None:
            term_integer = Get.next_fin_extension_id(
                self.__database, COLUMNS["legacy_term_id"])
            term_sct = self.__verhoeff.generateVerhoeff(term_integer, "11")

        en_row[COLUMNS["legacy_term_id"]] = f"{term_sn2}-{term_sct}"
        en_row[COLUMNS["term_id"]] = term_sct
        return en_row

    def __set_date(self, en_row: 'pd.Series'):
        en_row[COLUMNS["active"]] = "Y"
        en_row[COLUMNS["beginning_date"]] = self.__config.version_date
        en_row[COLUMNS["expiring_date"]] = self.__config.default_expiring_date
        return en_row

    def __create_lang_rows(self, en_row: 'pd.Series'):
        # create lang row for each language
        # each lang row get unique code_id
        # en_row_code_id is the parent_id and is the same for all lang rows - it is the code_id of the en_row
        # Everything else is the same as the en_row
        for lang in self.__config.langs:
            lang_row = en_row.copy()
            lang_row[COLUMNS["lang"]] = lang
            lang_row[COLUMNS["code_id"]] = Get.next_codeid(self.__database)
            lang_row[COLUMNS["en_row_code_id"]
                     ] = en_row[COLUMNS["code_id"]]
            self.__database = pd.concat(
                [self.__database, lang_row.to_frame().T], ignore_index=True)

    def commit(self):
        for _, en_row in self.__new_en_rows.iterrows():
            en_row = self.__set_code_id(en_row)
            en_row = self.__set_concept_id(en_row)
            en_row = self.__set_term_id(en_row)
            en_row = self.__set_date(en_row)
            self.__database = pd.concat(
                [self.__database, en_row.to_frame().T], ignore_index=True)
            self.__create_lang_rows(en_row)
        return self.__database
