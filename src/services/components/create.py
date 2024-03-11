import pandas as pd


class Create:
    @staticmethod
    def bundles(rows: 'pd.DataFrame'):
        bundles = []
        for i in set(rows['sct_termid_en']):
            bundles.append(rows[rows['sct_termid_en'] == i])
        return bundles
    
    @staticmethod
    def en_row(table: 'pd.DataFrame', new_row: int, new_lineid: int):
        new_row['lineid'] = new_lineid
        new_row['in_use'] = 'Y'
        new_row = new_row.to_frame().T
        return pd.concat([table, new_row], ignore_index=True)
