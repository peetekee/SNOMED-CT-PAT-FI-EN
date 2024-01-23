import re
import pandas as pd


class Component:
    def __init__(self, config) -> None:
        self.__config = config

    def is_en_row(self, row: 'pd.Series'):
        return row["lang"] == 'en'

    def bundle_has_en_row(self, bundle: 'pd.DataFrame'):
        return not bundle[bundle["lang"] == 'en'].empty

    def check_component_parentid(self, en_row: 'pd.Series', lang_rows: 'pd.DataFrame', table: 'pd.DataFrame'):
        parentid = en_row['lineid']
        table.at[en_row.index, 'sct_termid_en'] = parentid
        for lang_row in lang_rows.itertuples():
            table.at[lang_row.Index, 'sct_termid_en'] = parentid
        return table

    def empty_status_column(self, table: 'pd.DataFrame'):
        table['status'] = None
        return table
