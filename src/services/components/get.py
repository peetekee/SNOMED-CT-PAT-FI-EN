import re
import pandas as pd
from config import COLUMNS


class Get:
    @staticmethod
    def edit_rows(table: 'pd.DataFrame'):
        return table[table[COLUMNS["status"]] == "edit"].copy()

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
        return table[table[COLUMNS["en_row_code_id"]] == int(en_row[COLUMNS["en_row_code_id"]])].copy()

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


        
