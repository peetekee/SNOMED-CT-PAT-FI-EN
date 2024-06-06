import pandas as pd
from config import COLUMNS
from services import Get, Set, Post, Verhoeff


class New:
    """Class for creating new rows

    This class is used to create new rows in the database.
    It takes the database, the new en rows and the configuration as input and creates the new rows
    accordingly in the database.

    Can have predefined intl ids
    If neccessary, generates new national ids for the new rows.
    """

    def __init__(self, database: 'pd.DataFrame', new_en_rows: 'pd.DataFrame', config: object) -> None:
        self.__database = database
        self.__new_en_rows = new_en_rows
        self.__verhoeff = Verhoeff()
        self.__config = config

    def __generate_concept_id(self, en_row: 'pd.Series') -> 'pd.Series':
        """Generates or takes the concept id for the new en row

        Here the legacy concept id column is the so called master column
        that decides if the new row gets a new concept id or takes the old one.
        If the new row has no concept id, it generates a new national concept id.
        If the new row has a concept id, it takes that and copies it to the new rows.

        The concept ids are copied to lang rows later on.

        Args:
            en_row (pd.Series): The new row

        Raises:
            Exception: Has to have sn2 part

        Returns:
            pd.Series: The new en row with new concept id.
        """

        concept_sn2, concept_sct = Get.legacyid(
            en_row[COLUMNS["legacy_concept_id"]])
        if concept_sn2 == None:
            raise Exception(
                "One of the new rows has missing or invalid legacy conceptid SN2 part")
        if concept_sct == None:
            concept_integer = Get.next_fin_extension_id(
                self.__database, COLUMNS["concept_id"])
            concept_sct = self.__verhoeff.generateVerhoeff(
                concept_integer, "10")

        en_row[COLUMNS["legacy_concept_id"]] = f"{concept_sn2}-{concept_sct}"
        en_row[COLUMNS["concept_id"]] = concept_sct
        return en_row

    def __generate_term_id(self, en_row: 'pd.Series') -> 'pd.Series':
        """Generates the term id for the new en row

        The term id is copied to lang rows later on.

        Args:
            en_row (pd.Series): The new row

        Raises:
            Exception: Has to have sn2 part

        Returns:
            pd.Series: The new en row with new term id.
        """
        
        term_sn2, term_sct = Get.legacyid(en_row[COLUMNS["legacy_term_id"]])
        if term_sn2 == None:
            raise Exception(
                "One of the new rows has missing or invalid legacy termid SN2 part")
        if term_sct == None:
            term_integer = Get.next_fin_extension_id(
                self.__database, COLUMNS["term_id"])
            term_sct = self.__verhoeff.generateVerhoeff(term_integer, "11")

        en_row[COLUMNS["legacy_term_id"]] = f"{term_sn2}-{term_sct}"
        en_row[COLUMNS["term_id"]] = term_sct
        return en_row

    def __set_en_row(self, en_row: 'pd.Series') -> 'pd.Series':
        """Handles the new en row

        calls the functions to generate appropriate ids and adds the row to the database.
        Sets the en row code id and date.
        Generates the concept and term ids.

        Args:
            en_row (pd.Series): The new en row

        Returns:
            pd.Series: Returns the new en row for the lang rows.
        """

        en_row = Set.en_row_code_id(en_row, self.__database)
        en_row = Set.date(en_row, self.__config)
        en_row = self.__generate_concept_id(en_row)
        en_row = self.__generate_term_id(en_row)
        self.__database = Post.new_row_to_database_table(
            en_row, self.__database)
        return en_row

    def __create_lang_rows(self, en_row: 'pd.Series') -> None:
        """Creates the lang rows for the new en row

        Basically copies the en row and changes the lang column.

        Args:
            en_row (pd.Series): The new en row
        """

        for lang in self.__config.langs:
            lang_row = en_row.copy()
            lang_row[COLUMNS["lang"]] = lang
            lang_row[COLUMNS["code_id"]] = Get.next_codeid(self.__database)
            lang_row[COLUMNS["en_row_code_id"]
                     ] = en_row[COLUMNS["code_id"]]
            self.__database = Post.new_row_to_database_table(
                lang_row, self.__database)

    def commit(self) -> 'pd.DataFrame':
        """Main function

        Returns:
            pd.DataFrame: The updated database
        """

        for _, en_row in self.__new_en_rows.iterrows():
            # set en row lang to en
            en_row[COLUMNS["lang"]] = "en"
            en_row = self.__set_en_row(en_row)
            self.__create_lang_rows(en_row)
        return self.__database
