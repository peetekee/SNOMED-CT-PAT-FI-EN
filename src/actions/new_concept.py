import pandas as pd
from config import COLUMNS
from services import Get, Put, Set, Post, Verhoeff
from .fsn import FSN


class NewConcept:
    """Class for editing concepts

    This class is used to edit concepts in the database.
    It takes the database, the new concept rows and the configuration as input and edits the concepts
    accordingly in the database.

    It inactivates the old concept and creates a new concept with the new values.
    """

    def __init__(self, database: 'pd.DataFrame', new_concept_en_rows: 'list', config: object) -> None:
        self.__database = database
        self.__new_concept_en_rows = new_concept_en_rows
        self.__verhoeff = Verhoeff()
        self.__config = config

    def __set_concept_id(self, new_en_row: 'pd.Series') -> tuple:
        """Sets the concept id and the legacy concept id for the new concept row

        If the new concept row has no concept id, it generates a national new concept id.
        On the other hand, if the new concept row has a concept id, it copies takes that
        and copies it to the new concept rows

        New concept id is generated by taking the next available concept id from the database
        and generating a SCTID for it.

        Args:
            new_en_row (pd.Series): The en row of the new concept

        Raises:
            Exception: If the new concept row has missing or invalid legacy conceptid SN2 part

        Returns:
            tuple: The new concept row and the SN2 part of the legacy concept id
        """

        concept_sn2, concept_sct = Get.legacyid(
            new_en_row[COLUMNS["legacy_concept_id"]])
        if concept_sn2 in self.__config.empty_values:
            raise Exception(
                "One of the new_concept rows has missing or invalid legacy conceptid SN2 part")
        if concept_sct in self.__config.empty_values:
            concept_integer = Get.next_fin_extension_id(
                self.__database, COLUMNS["concept_id"])
            concept_sct = self.__verhoeff.generateVerhoeff(
                concept_integer, "10")

        new_en_row[COLUMNS["legacy_concept_id"]
                   ] = f"{concept_sn2}-{concept_sct}"
        new_en_row[COLUMNS["concept_id"]] = concept_sct
        return new_en_row

    def __set_en_row(self, new_en_row: 'pd.Series', old_en_row: 'pd.Series') -> 'pd.Series':
        """Sets the en row for the new concept

        Calls the necessary functions to set the en row for the new concept.
        Inactivates the old en row and adds the new en row to the database.
        Returns the new en row for handling the lang rows.

        Args:
            new_en_row (pd.Series): The new en row
            old_en_row (pd.Series): The old en row from the database

        Returns:
            pd.Series: The new en row
        """

        new_en_row = Set.en_row_code_id(new_en_row, self.__database)
        new_en_row = Set.date(new_en_row, self.__config)
        new_en_row = Set.administrative(new_en_row, old_en_row, self.__config)
        new_en_row = self.__set_concept_id(new_en_row)
        new_en_row = Set.term_id(new_en_row, old_en_row, self.__database,
                                 self.__verhoeff, self.__config)
        new_en_row = Set.fsn(new_en_row, old_en_row, self.__config)
        new_en_row = Set.term(new_en_row, old_en_row, self.__config)
        self.__database = FSN(self.__database, new_en_row.to_frame().transpose(), True).commit()
        # inactivate the old en row
        self.__database = Put.inactivate_row(old_en_row[COLUMNS["code_id"]], self.__database, self.__config.version_date,
                                              old_en_row[COLUMNS["inaktivoinnin_selite"]], old_en_row[COLUMNS["edit_comment"]], new_en_row[COLUMNS["code_id"]])
        self.__database = Post.new_row_to_database_table(
            new_en_row, self.__database)
        return new_en_row

    def __set_lang_rows(self, new_en_row: 'pd.Series', old_en_row: 'pd.Series') -> None:
        """Sets the lang rows for the new concept

        Gets the en row, creates a new lang row and inactivates the old lang row.
        Adds the new lang row to the database.

        Checks if the old lang row term id is the same as the old en row term id.
        If it is, sets the new lang row term and term ids to the new en row term ids.
        If it isn't, gets the SN2 from the new en row and sets the new lang row term id.

        Args:
            new_en_row (pd.Series): The new en row
            old_en_row (pd.Series): The old en row from the database
        """

        old_lang_rows = Get.lang_rows_by_en(self.__database, old_en_row)
        for _, old_lang_row in old_lang_rows.iterrows():
            new_lang_row = old_lang_row.copy()
            new_lang_row[COLUMNS["code_id"]] = Get.next_codeid(self.__database)
            new_lang_row = Set.lang_row_concept_columns(
                new_lang_row, new_en_row)
            new_lang_row[COLUMNS["edit_comment"]] = new_en_row[COLUMNS["edit_comment"]]
            # check if the old lang row term id is the same as the old en row term id
            # if it is, set the new lang row term and term ids to the new en row term ids
            if old_lang_row[COLUMNS["legacy_term_id"]] == old_en_row[COLUMNS["legacy_term_id"]]:
                new_lang_row[COLUMNS["legacy_term_id"]
                             ] = new_en_row[COLUMNS["legacy_term_id"]]
                new_lang_row[COLUMNS["term_id"]
                             ] = new_en_row[COLUMNS["term_id"]]
                new_lang_row[COLUMNS["term"]] = new_en_row[COLUMNS["term"]]
            else:
                new_lang_row = Set.term_id(
                    new_lang_row, old_lang_row, self.__database, self.__verhoeff, self.__config, True)
            new_lang_row = Set.date(new_lang_row, self.__config)
            # inactivate the old lang row
            self.__database = Put.inactivate_row(old_lang_row[COLUMNS["code_id"]], self.__database, self.__config.version_date,
                                                  old_en_row[COLUMNS["inaktivoinnin_selite"]], old_en_row[COLUMNS["edit_comment"]], new_lang_row[COLUMNS["code_id"]])
            # add the new lang row to the database
            self.__database = Post.new_row_to_database_table(
                new_lang_row, self.__database)

    def commit(self) -> 'pd.DataFrame':
        """Main function for editing concepts

        Calls the necessary functions to edit the concepts in the database.

        Returns:
            pd.DataFrame: The edited database
        """

        for old_en_row, new_en_row in self.__new_concept_en_rows:
            new_en_row = self.__set_en_row(new_en_row, old_en_row)
            self.__set_lang_rows(new_en_row, old_en_row)
        return self.__database
