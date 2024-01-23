import pandas as pd


class Create:
    @staticmethod
    def create_bundles(rows: 'pd.DataFrame'):
        bundles = []
        for i in set(rows['sct_termid_en']):
            bundles.append(rows[rows['sct_termid_en'] == i])
        return bundles

    @staticmethod
    def create_new_codeids(next_lineid: int, how_many: int):
        return [i for i in range(next_lineid, next_lineid + how_many)]
