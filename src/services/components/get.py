import re
import pandas as pd
from collections import namedtuple
from config import COLUMNS, EDIT_TYPES


class Get:
    """Includes get methods that retrieve something

    Used by the actions to retrieve rows from the database.
    """
    @staticmethod
    def edit_rows(table: 'pd.DataFrame', database: 'pd.DataFrame') -> dict:
        """Get edit rows from the excel table

        The edit rows are the rows that have a value in the status column.
        and they are connected to the database by the codeid column.

        So old and new row have the same codeid but the new row has a value in the status column.

        The add robustness to the code, the old row is retrieved from the database.
        Only the columns relevant to the edit are copied from the excel.

        These columns are edit_comment and inaktivoinnin_selite.

        Args:
            table (pd.DataFrame): the excel table
            database (pd.DataFrame): the database or "kanta"

        Returns:
            dict: dictionary with edit types as keys and namedtuples as values
                    The namedtuples have old and new rows as values.
        """

        dict_edit_rows = {}
        RowPair = namedtuple('RowPair', ['old_row', 'new_row'])
        for edit_type in EDIT_TYPES:
            # create dictionary with edit_type as key and rows as value
            # for every edit type we have two rows that have the same codeid
            # the new one has a value in status column. The old one does not
            # create NamedTuple with old and new row
            edit_rows = table[table[COLUMNS["status"]] == edit_type].copy()

            dict_edit_rows[edit_type] = []
            if not edit_rows.empty:
                for _, new_row in edit_rows.iterrows():
                    # only one old row should exist
                    old_row = database[database[COLUMNS["code_id"]] == int(
                        new_row[COLUMNS["code_id"]])].iloc[0].copy()
                    excel_old_row = table[(table[COLUMNS["code_id"]] == new_row[COLUMNS["code_id"]]) & (
                        table[COLUMNS["status"]].isna())].iloc[0].copy()
                    old_row[COLUMNS["edit_comment"]
                            ] = excel_old_row[COLUMNS["edit_comment"]]
                    old_row[COLUMNS["inaktivoinnin_selite"]
                            ] = excel_old_row[COLUMNS["inaktivoinnin_selite"]]
                    # set the code_id to int
                    new_row[COLUMNS["code_id"]] = int(new_row[COLUMNS["code_id"]])
                    old_row[COLUMNS["code_id"]] = int(old_row[COLUMNS["code_id"]])
                    if "accept" in new_row:
                        if new_row["accept"] == "xterm":
                            concept_sn2, concept_sct = Get.legacyid(new_row[COLUMNS["legacy_term_id"]])
                            new_row[COLUMNS["legacy_term_id"]] = f"{concept_sn2}-"
                            new_row[COLUMNS["term"]] = old_row[COLUMNS["term"]]
                            dict_edit_rows["new_concept"].append(RowPair(old_row, new_row))
                        # elif new_row["accept"] == "n":
                        #     concept_sn2, concept_sct = Get.legacyid(new_row[COLUMNS["legacy_concept_id"]])
                        #     new_row[COLUMNS["legacy_concept_id"]] = f"{concept_sn2}-"
                        #     new_row[COLUMNS["legacy_term_id"]] = f"{concept_sn2}-"
                        #     dict_edit_rows["new_concept"].append(RowPair(old_row, new_row))
                        else:
                            dict_edit_rows[edit_type].append(RowPair(old_row, new_row))
                    else:
                        dict_edit_rows[edit_type].append(RowPair(old_row, new_row))
        return dict_edit_rows

    @staticmethod
    def new_rows(table: 'pd.DataFrame') -> 'pd.DataFrame':
        """Get new rows from the excel table

        Args:
            table (pd.DataFrame): Excel table

        Returns:
            pd.DataFrame: All of the new en rows
        """

        return table[table[COLUMNS["status"]] == "new"].copy()

    @staticmethod
    def fsn_rows(table: 'pd.DataFrame') -> 'pd.DataFrame':
        """Get fsn updates from the excel table.

        Args:
            table (pd.DataFrame): Excel table

        Returns:
            pd.DataFrame: All of the fsn update rows
        """

        fsn_rows = table[table[COLUMNS["status"]] == "fsn"].copy()
        fsn_rows[COLUMNS["code_id"]] = fsn_rows[COLUMNS["code_id"]].astype(int)
        return fsn_rows

    @staticmethod
    def activated_rows(table: 'pd.DataFrame') -> 'pd.DataFrame':
        """Get activated rows from the excel table.

        Args:
            table (pd.DataFrame): Excel table

        Returns:
            pd.DataFrame: All of the activated rows
        """
        activated_rows = table[table[COLUMNS["status"]] == "activated"].copy()
        activated_rows[COLUMNS["code_id"]] = activated_rows[COLUMNS["code_id"]].astype(int)
        return activated_rows

    @staticmethod
    def inactivated_rows(table: 'pd.DataFrame') -> 'pd.DataFrame':
        """Get inactivated rows from the excel table.

        Args:
            table (pd.DataFrame): Excel table

        Returns:
            pd.DataFrame: All of the inactivated rows
        """

        inactivated_rows = table[table[COLUMNS["status"]] == "inactivate"].copy()
        inactivated_rows[COLUMNS["code_id"]] = inactivated_rows[COLUMNS["code_id"]].astype(int)
        return inactivated_rows
    
    @staticmethod
    def administrative_rows(table: 'pd.DataFrame') -> 'pd.DataFrame':
        """Get administrative rows from the excel table.

        Args:
            table (pd.DataFrame): Excel table

        Returns:
            pd.DataFrame: All of the administrative rows
        """

        administrative_rows = table[table[COLUMNS["status"]] == "administrative"].copy()
        administrative_rows[COLUMNS["code_id"]] = administrative_rows[COLUMNS["code_id"]].astype(int)
        return administrative_rows

    @staticmethod
    def en_row(table: 'pd.DataFrame') -> 'pd.DataFrame':
        """Get en rows from the excel table.

        Args:
            table (pd.DataFrame): Excel table

        Returns:
            pd.DataFrame: All of the en rows
        """

        return table[table[COLUMNS["lang"]] == 'en'].copy()

    @staticmethod
    def lang_rows_by_en(table: 'pd.DataFrame', en_row: 'pd.DataFrame') -> 'pd.DataFrame':
        """Get lang rows by en row from the database

        Retrieves the lang rows from the database that have the same en_row_code_id as the en row code_id.

        Args:
            table (pd.DataFrame): The database
            en_row (pd.DataFrame): The en row

        Returns:
            pd.DataFrame: The lang rows associated with the en row
        """

        return table[(table[COLUMNS["en_row_code_id"]] == en_row[COLUMNS["en_row_code_id"]]) & (table[COLUMNS["lang"]] != "en")].copy()

    @staticmethod
    def index_by_codeid(table: 'pd.DataFrame', code_id: int) -> int:
        """Get the index of a row by codeid

        The dataframes have dedicated unique index columns.
        This function is used to get the index of a row by codeid.

        This ensures that in the midst of the update the correct row is updated.

        Args:
            table (pd.DataFrame): the database
            code_id (int): The codeid of the row we want the index of

        Returns:
            int: The DataFrame index of the row
        """
        return table.loc[table[COLUMNS["code_id"]] == int(code_id)].index.values[0]

    @staticmethod
    def next_codeid(table: 'pd.DataFrame') -> int:
        """Retrieves the next available codeid from the database

        Args:
            table (pd.DataFrame): The database

        Returns:
            int: The next available codeid
        """
        return int(table[COLUMNS["code_id"]].astype(int).max() + 1)

    @staticmethod
    def legacyid(legacyid: str) -> tuple:
        """Get the sn2 and sct_id from the legacyid

        legayid is our own national invention and does not exist in the SNOMED standard.
        It was done based on the wishes from the field.

        The legacyid is a combination of sn2 and sct_id separated by a '-'.
        The sn2 is the first part and the sct_id is the second part.

        sn2 means SNOMED 2 which is the old SNOMED version that is the previous
        terminology used in laboratory information systems.

        sct means SNOMED CT which is the new SNOMED version that we are
        moving to.

        We are keeping the old SNOMED2 codes in the database for reference
        and for the transition period.

        Args:
            legacyid (str): The legacyid, can be either legacy term or concept id.

        Returns:
            tuple: The sn2 and sct_id
        """

        if not re.fullmatch(r".+-\d*", legacyid):
            return None
        sn2, sct_id = legacyid.split('-')
        return sn2 or None, sct_id or None

    @staticmethod
    def next_fin_extension_id(table: 'pd.DataFrame', column: str) -> int:
        """Get the next available fin extension id

        We have our own national code space that is used for the finnish extensions.
        The finnish extensions are used for the national codes that are not in the SNOMED standard.

        This function retrieves the next available fin extension id from the database.

        Args:
            table (pd.DataFrame): The database
            column (str): The column that contains the fin extension ids. Either sct_term_id or sct_concept_id

        Returns:
            int: The next available fin extension id
        """

        fin_id_series = table[column][table[column].str.fullmatch(
            r"^\d+1000288(10|11)\d$") == True]
        fin_id_max = 0
        if not fin_id_series.empty:
            fin_id_series = fin_id_series.apply(lambda x: x[:len(x)-10])
            fin_id_series = fin_id_series.astype(int)
            fin_id_max = fin_id_series.max()
        fin_id_max += 1
        return fin_id_max
