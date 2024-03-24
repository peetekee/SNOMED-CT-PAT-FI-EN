import re
import pandas as pd
from collections import namedtuple
from config import Config, COLUMNS, EDIT_TYPES


class Get:
    @staticmethod
    def edit_rows(table: 'pd.DataFrame', database: 'pd.DataFrame'):
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
                    old_row = database[database[COLUMNS["code_id"]] == int(new_row[COLUMNS["code_id"]])].iloc[0].copy()
                    table_old_row = table[(table[COLUMNS["code_id"]] == new_row[COLUMNS["code_id"]]) & (table[COLUMNS["status"]].isna())].iloc[0].copy()
                    old_row[COLUMNS["edit_comment"]] = table_old_row[COLUMNS["edit_comment"]]
                    old_row[COLUMNS["inaktivoinnin_selite"]] = table_old_row[COLUMNS["inaktivoinnin_selite"]]
                    # get comment and inaktivoinnin_selite from old row
                    # from the table dataframe

                    # Create a namedtuple with old and new row
                    dict_edit_rows[edit_type].append(RowPair(old_row, new_row))
        return dict_edit_rows

    @staticmethod
    def new_rows(table: 'pd.DataFrame'):
        return table[table[COLUMNS["status"]] == "new"].copy()
    
    @staticmethod
    def fsn_rows(table: 'pd.DataFrame'):
        return table[table[COLUMNS["status"]] == "fsn"].copy()

    @staticmethod
    def activated_rows(table: 'pd.DataFrame'):
        return table[table[COLUMNS["status"]] == "activated"].copy()

    @staticmethod
    def inactivated_rows(table: 'pd.DataFrame'):
        return table[table[COLUMNS["status"]] == "inactivate"].copy()

    @staticmethod
    def en_row(table: 'pd.DataFrame'):
        return table[table[COLUMNS["lang"]] == 'en'].copy()

    @staticmethod
    def lang_rows(table: 'pd.DataFrame'):
        return table[table['lang'] != 'en'].copy()

    @staticmethod
    def lang_rows_by_en(table: 'pd.DataFrame', en_row: 'pd.DataFrame'):
        return table[(table[COLUMNS["en_row_code_id"]] == en_row[COLUMNS["en_row_code_id"]]) & (table[COLUMNS["lang"]] != "en")].copy()

    @staticmethod
    def old_row(table: 'pd.DataFrame'):
        return table[table['status'] != 'edit'].iloc[0]

    @staticmethod
    def new_row(table: 'pd.DataFrame'):
        return table[table['status'] == 'edit'].iloc[0]

    @staticmethod
    def table_index(table: 'pd.DataFrame', row: 'pd.DataFrame'):
        return table.loc[table[COLUMNS["code_id"]] ==
                         row['lineid']].index[0]

    @staticmethod
    def index_by_codeid(table: 'pd.DataFrame', lineid: int):
        return table.loc[table[COLUMNS["code_id"]] == int(lineid)].index.values[0]

    @staticmethod
    def row_by_codeid(table: 'pd.DataFrame', lineid: int):
        return table[table['lineid'] == lineid].copy()

    @staticmethod
    def row_by_index(table: 'pd.DataFrame', index: int):
        return table.iloc[index].copy()

    @staticmethod
    def next_codeid(table: 'pd.DataFrame'):
        return int(table[COLUMNS["code_id"]].astype(int).max() + 1)

    @staticmethod
    def legacyid(legacyid: str):
        if not re.fullmatch(r".+-\d*", legacyid):
            return None
        sn2, sct_id = legacyid.split('-')
        return sn2 or None, sct_id or None
    
    @staticmethod
    def next_fin_extension_id(table: 'pd.DataFrame', column: str) -> int:
        fin_id_series = table[column][table[column].str.fullmatch(
            r"^\d+1000288(10|11)\d$") == True]
        fin_id_max = 0
        if not fin_id_series.empty:
            fin_id_series = fin_id_series.apply(lambda x: x[:len(x)-10])
            fin_id_series = fin_id_series.astype(int)
            fin_id_max = fin_id_series.max()
        fin_id_max += 1
        return fin_id_max
    
    @staticmethod
    def bundles(row: 'pd.DataFrame', database: 'pd.DataFrame'):
        """Get all rows associated with an en-row

        Use sct_termdid_en which is the same 

        Args:
            row (pd.DataFrame): _description_
            database (pd.DataFrame): _description_

        Returns:
            _type_: _description_
        """
        bundles = []
        for lineid in set(row['sct_termid_en']):
            bundles.append(database[database['sct_termid_en'] == lineid])
        return bundles
    
    @staticmethod
    def edit_en_row_pairs(table: 'pd.DataFrame', status_value: str):
        edit_rows = table[table[COLUMNS["status"]] == status_value].copy()
        # Get all the old rows and create the namedtuples
        edit_en_row_pairs = []
        for _, row in edit_rows.iterrows():
            # only one old row should exist
            old_row = table[table[COLUMNS["code_id"]] == row[COLUMNS["en_row_code_id"]]].iloc[0].copy()
            edit_en_row_pairs.append((old_row, row))
        
        return edit_en_row_pairs


        
