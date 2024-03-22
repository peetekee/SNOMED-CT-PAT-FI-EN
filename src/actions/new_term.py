import pandas as pd
from config import COLUMNS, Config
from services.components import Get, Put
from services.general import Verhoeff


class NewTerm:

    COPY_COLUMNS = [
        COLUMNS["tmdc"],
        COLUMNS["lang"],
        COLUMNS["tays_snomed_ii"],
        COLUMNS["parent_concept_id"],
        COLUMNS["parent_concept_fsn"],
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
        COLUMNS["verenkierto_yleiset"]
    ]

    def __init__(self, database: 'pd.DataFrame', new_term_en_rows: 'list'):
        self.__database = database
        self.__new_term_en_rows = new_term_en_rows
        self.__verhoeff = Verhoeff()
        self.__config = Config()

    def __set_code_id(self, new_en_row: 'pd.Series'):
        new_en_row[COLUMNS["code_id"]] = Get.next_codeid(self.__database)
        new_en_row[COLUMNS["en_row_code_id"]] = new_en_row[COLUMNS["code_id"]]
        return new_en_row

    def __set_date(self, new_en_row: 'pd.Series'):
        new_en_row[COLUMNS["active"]] = "Y"
        new_en_row[COLUMNS["beginning_date"]] = self.__config.version_date
        new_en_row[COLUMNS["expiring_date"]
                   ] = self.__config.default_expiring_date
        return new_en_row

    def __set_administrative(self, new_en_row: 'pd.Series', old_en_row: 'pd.Series'):
        for column in self.COPY_COLUMNS:
            # if the new rows has no value, copy the value from the old row
            if new_en_row[column] in self.__config.empty_values:
                new_en_row[column] = old_en_row[column]
        return new_en_row

    def __set_term_id(self, new_en_row: 'pd.Series', old_en_row: 'pd.Series'):
        term_sn2, term_sct = Get.legacyid(new_en_row[COLUMNS["legacy_term_id"]])
        if term_sn2 == None:
            raise Exception(
                "One of the new rows has missing or invalid legacy termid SN2 part")
        if term_sct == None:
            term_integer = Get.next_fin_extension_id(
                self.__database, COLUMNS["legacy_term_id"])
            term_sct = self.__verhoeff.generateVerhoeff(term_integer,"11")

        new_en_row[COLUMNS["legacy_term_id"]] = f"{term_sn2}-{term_sct}"
        new_en_row[COLUMNS["term_id"]] = term_sct
        return new_en_row

    def __set_fsn(self, new_en_row: 'pd.Series', old_en_row: 'pd.Series'):
        # if the new rows has no value, copy the value from the old row
        if pd.isnull(new_en_row[COLUMNS["concept_fsn"]]):
            new_en_row[COLUMNS["concept_fsn"]
                       ] = old_en_row[COLUMNS["concept_fsn"]]
        return new_en_row

    def __set_en_row(self, new_en_row: 'pd.Series', old_en_row: 'pd.Series'):
        new_en_row = self.__set_code_id(new_en_row)
        new_en_row = self.__set_date(new_en_row)
        new_en_row = self.__set_administrative(new_en_row, old_en_row)
        new_en_row = self.__set_term_id(new_en_row, old_en_row)
        new_en_row = self.__set_fsn(new_en_row, old_en_row)
        # inactivate the old en row
        index = Get.index_by_codeid(
            self.__database, old_en_row[COLUMNS["code_id"]])
        self.__database = Put.inactivated_row(self.__database, index, self.__config.version_date,
                                              old_en_row[COLUMNS["inaktivoinnin_selite"]], old_en_row[COLUMNS["edit_comment"]], new_en_row[COLUMNS["code_id"]])
        self.__database = pd.concat(
            [self.__database, new_en_row.to_frame().T], ignore_index=True)
        return new_en_row
    
    def __set_lang_rows(self, new_en_row: 'pd.Series', old_en_row: 'pd.Series'):
        old_lang_rows = Get.lang_rows_by_en(self.__database, old_en_row)
        for _, old_lang_row in old_lang_rows.iterrows():
            new_lang_row = old_lang_row.copy()
            new_lang_row[COLUMNS["code_id"]] = Get.next_codeid(self.__database)
            new_lang_row[COLUMNS["en_row_code_id"]
                         ] = new_en_row[COLUMNS["code_id"]]
            new_lang_row[COLUMNS["legacy_concept_id"]
                         ] = new_en_row[COLUMNS["legacy_concept_id"]]
            new_lang_row[COLUMNS["concept_id"]
                         ] = new_en_row[COLUMNS["concept_id"]]
            new_lang_row[COLUMNS["concept_fsn"]
                         ] = new_en_row[COLUMNS["concept_fsn"]]
            # check if the old lang row term id is the same as the old en row term id
            # if it is, set the new lang row term and term ids to the new en row term ids
            if old_lang_row[COLUMNS["legacy_term_id"]] == old_en_row[COLUMNS["legacy_term_id"]]:
                new_lang_row[COLUMNS["legacy_term_id"]
                             ] = new_en_row[COLUMNS["legacy_term_id"]]
                new_lang_row[COLUMNS["term_id"]
                             ] = new_en_row[COLUMNS["term_id"]]
                new_lang_row[COLUMNS["term"]] = new_en_row[COLUMNS["term"]]
            else:
                new_lang_row = self.__set_term_id(new_lang_row, old_en_row)
            new_lang_row = self.__set_date(new_lang_row)
            # inactivate the old lang row
            index = Get.index_by_codeid(
                self.__database, old_lang_row[COLUMNS["code_id"]])
            self.__database = Put.inactivated_row(self.__database, index, self.__config.version_date,
                                                  old_en_row[COLUMNS["inaktivoinnin_selite"]], old_en_row[COLUMNS["edit_comment"]], new_lang_row[COLUMNS["code_id"]])
            # add the new lang row to the database
            self.__database = pd.concat(
                [self.__database, new_lang_row.to_frame().T], ignore_index=True)

    def commit(self):
        for new_en_row, old_en_row in self.__new_term_en_rows:
            new_en_row = self.__set_en_row(new_en_row, old_en_row)
            self.__set_lang_rows(new_en_row, old_en_row)
        return self.__database