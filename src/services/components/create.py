import pandas as pd


class Create:
    @staticmethod
    def bundles(rows: 'pd.DataFrame'):
        bundles = []
        for i in set(rows['sct_termid_en']):
            bundles.append(rows[rows['sct_termid_en'] == i])
        return bundles

    @staticmethod
    def new_codeids(next_lineid: int, how_many: int):
        return [i for i in range(next_lineid, next_lineid + how_many)]
    
    @staticmethod
    def new_row(table: 'pd.DataFrame', new_row: int, new_lineid: int):
        new_row['lineid'] = new_lineid
        new_row['in_use'] = 'Y'
        new_row = new_row.to_frame().T
        return pd.concat([table, new_row], ignore_index=True)
