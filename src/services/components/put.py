import pandas as pd
from config import COLUMNS


class Put:
    @staticmethod
    def inactivated_row(table: 'pd.DataFrame', index: int, expiring_date: str, inaktivoinnin_selite: str, edit_comment: str):
        table.loc[index, COLUMNS["active"]] = "N"
        table.loc[index, COLUMNS["expiring_date"]] = expiring_date
        table.loc[index, COLUMNS["inaktivoinnin_selite"]] = inaktivoinnin_selite
        table.loc[index, COLUMNS["edit_comment"]] = edit_comment
        return table

    @staticmethod
    def activated_row(table: 'pd.DataFrame', activated_row: 'pd.Series', index: int):
        table.loc[index, 'in_use'] = 'Y'
        table.loc[index, 'effectivetime'] = activated_row['effectivetime']
        table.loc[index, 'supersededtime'] = activated_row['supersededtime']
        table.loc[index, 'inaktivoinnin_selite'] = None
        return table
    
    # @staticmethod
    # def handle_old_row(table: 'pd.DataFrame', old_row: 'pd.Series', index: int, new_lineid: int):
    #     table.loc[index, :] = old_row[:]
    #     table.loc[index, 'in_use'] = 'N'
    #     table.loc[index, 'superseded_by'] = new_lineid
    #     return table
