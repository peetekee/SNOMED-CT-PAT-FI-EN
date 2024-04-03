import pandas as pd
from config import COLUMNS, COPY_COLUMNS
from .get import Get


class Set:
    """This class is used to set values in columns
    """

    @staticmethod
    def en_row_code_id(en_row: 'pd.Series', database: 'pd.DataFrame') -> 'pd.Series':
        """Sets the code id of the en row

        Gets the next code id from the database and sets it to the en row.

        Args:
            en_row (pd.Series): The en row
            database (pd.DataFrame): The database

        Returns:
            pd.Series: The en row with the code id set
        """

        en_row[COLUMNS["code_id"]] = Get.next_codeid(database)
        en_row[COLUMNS["en_row_code_id"]] = en_row[COLUMNS["code_id"]]
        return en_row

    @staticmethod
    def term_id(new_row: 'pd.Series', old_row: 'pd.Series', database: 'pd.DataFrame', verhoeff: object, config: object, concept_change=False) -> 'pd.Series':
        """Sets the term id of the new row

        If the term id is missing or invalid, it generates a new term id.
        If the term id is the same as the old term id and the term is different,
        it generates a new term id.

        Args:
            new_row (pd.Series): The new row
            old_row (pd.Series): The associated old row from the database
            database (pd.DataFrame): The database
            verhoeff (_type_): Class for generating verhoeff ids, standard to SNOMED CT
            config (object): The configuration class

        Raises:
            Exception: One of the edit rows has missing or invalid legacy termid SN2 part

        Returns:
            pd.Series: The new row with the term id set
        """

        new_term_sn2, new_term_sct = Get.legacyid(
            new_row[COLUMNS["legacy_term_id"]])
        _, old_term_sct = Get.legacyid(
            old_row[COLUMNS["legacy_term_id"]])
        if new_term_sn2 in config.empty_values:
            raise Exception(
                "One of the edit rows has missing or invalid legacy termid SN2 part")
        if new_term_sct in config.empty_values or concept_change:
            new_term_int = Get.next_fin_extension_id(
                database, COLUMNS["term_id"])
            new_term_sct = verhoeff.generateVerhoeff(new_term_int, "11")
        new_row[COLUMNS["legacy_term_id"]] = f"{new_term_sn2}-{new_term_sct}"
        new_row[COLUMNS["term_id"]] = new_term_sct
        return new_row

    @staticmethod
    def lang_row_concept_columns(new_row: 'pd.Series', en_row: 'pd.Series') -> 'pd.Series':
        """Sets the concept columns of the lang rows

        They are the same for all lang rows.
        The concept columns are copied from the en row to the lang row.
        And the lang rows are bounded to the en row with the en_row_code_id.

        Args:
            new_row (pd.Series): The new row
            en_row (pd.Series): The en row

        Returns:
            pd.Series: The new row with the concept columns set
        """
        new_row[COLUMNS["en_row_code_id"]] = en_row[COLUMNS["code_id"]]
        new_row[COLUMNS["legacy_concept_id"]
                ] = en_row[COLUMNS["legacy_concept_id"]]
        new_row[COLUMNS["concept_id"]] = en_row[COLUMNS["concept_id"]]
        new_row[COLUMNS["concept_fsn"]] = en_row[COLUMNS["concept_fsn"]]
        return new_row

    @staticmethod
    def date(row: 'pd.Series', config: object) -> 'pd.Series':
        """Sets the beginning and expiring dates of the row

        Args:
            row (pd.Series): Target row
            config (object): The configuration class to get the dates.

        Returns:
            pd.Series: The row with the dates set
        """
        row[COLUMNS["active"]] = "Y"
        row[COLUMNS["beginning_date"]] = config.version_date
        row[COLUMNS["expiring_date"]
            ] = config.default_expiring_date
        return row

    @staticmethod
    def administrative(new_row: 'pd.Series', old_row: 'pd.Series', config: object) -> 'pd.Series':
        """Sets the administrative columns of the new row

        The administrative columns are copied from the old row to the new row.
        The administrative columns are not visible to the end-users and are for internal use only.
        In practise they are not visible in the koodistopalvelu.
        They are for the pathologists and the developers.

        Args:
            new_row (pd.Series): The new row
            old_row (pd.Series): The old row from the database
            config (object): The configuration class

        Returns:
            pd.Series: The new row with the administrative columns set
        """

        for column in COPY_COLUMNS:
            if new_row[column] in config.empty_values:
                new_row[column] = old_row[column]
        return new_row

    @staticmethod
    def lang_administrative(en_row: 'pd.Series', lang_row: 'pd.Series', columns: list) -> 'pd.Series':
        """Sets the administrative columns of the new lang row

        The administrative columns are copied from the old row to the new row.
        The administrative columns are not visible to the end-users and are for internal use only.
        In practise they are not visible in the koodistopalvelu.
        They are for the pathologists and the developers.

        Args:
            new_row (pd.Series): The new row
            old_row (pd.Series): The old row from the database
            config (object): The configuration class

        Returns:
            pd.Series: The new row with the administrative columns set
        """

        for column in columns:
            lang_row[column] = en_row[column]
        return lang_row

    @staticmethod
    def fsn(new_row: 'pd.Series', old_row: 'pd.Series', config: object) -> 'pd.Series':
        """Sets the fully specified name of the new row

        Args:
            new_row (pd.Series): The new row
            old_row (pd.Series): The old row from the database
            config (object): The configuration class

        Returns:
            pd.Series: The new row with the fully specified name set
        """

        if new_row[COLUMNS["concept_fsn"]] in config.empty_values:
            new_row[COLUMNS["concept_fsn"]] = old_row[COLUMNS["concept_fsn"]]
        return new_row

    @staticmethod
    def term(new_row: 'pd.Series', old_row: 'pd.Series', config: object) -> 'pd.Series':
        """Sets the term of the new row

        Args:
            new_row (pd.Series): The new row
            old_row (pd.Series): The old row from the database
            config (object): The configuration class

        Returns:
            pd.Series: The new row with the term set
        """

        if new_row[COLUMNS["term"]] in config.empty_values:
            new_row[COLUMNS["term"]] = old_row[COLUMNS["term"]]
        return new_row

    @staticmethod
    def empty_status_column(table: 'pd.DataFrame') -> 'pd.DataFrame':
        """Sets the status column to empty

        Args:
            table (pd.DataFrame): The table

        Returns:
            pd.DataFrame: The table with the status column set to empty
        """

        table[COLUMNS["status"]] = ""
        return table
