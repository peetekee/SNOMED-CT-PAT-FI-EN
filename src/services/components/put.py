import pandas as pd
from config import COLUMNS


class Put:
    @staticmethod
    def inactivated_row(table: 'pd.DataFrame', index: int, expiring_date: str, inaktivoinnin_selite: str, edit_comment: str, korvaava_koodi = ""):
        table.loc[index, COLUMNS["active"]] = "N"
        table.loc[index, COLUMNS["expiring_date"]] = expiring_date
        table.loc[index, COLUMNS["inaktivoinnin_selite"]] = inaktivoinnin_selite
        table.loc[index, COLUMNS["edit_comment"]] = edit_comment
        table.loc[index, COLUMNS["korvaava_koodi"]] = korvaava_koodi
        return table

    @staticmethod
    def activated_row(table: 'pd.DataFrame', index: int, beginning_date: str, expiring_date: str, edit_comment: str):
        table.loc[index, COLUMNS["active"]] = "Y"
        table.loc[index, COLUMNS["beginning_date"]] = beginning_date
        table.loc[index, COLUMNS["expiring_date"]] = expiring_date
        table.loc[index, COLUMNS["inaktivoinnin_selite"]] = None
        table.loc[index, COLUMNS["edit_comment"]] = edit_comment
        return table
    
    @staticmethod
    def fsn(table: 'pd.DataFrame', index: int, new_fsn: str, edit_comment: str):
        table.loc[index, COLUMNS["concept_fsn"]] = new_fsn
        table.loc[index, COLUMNS["edit_comment"]] = edit_comment
        return table
    
    @staticmethod
    def administrative_columns(table: 'pd.DataFrame', index: int, en_row: 'pd.Series', administrative_columns: list[str]):
        for column in administrative_columns:
            table.loc[index, column] = en_row[column]
        return table
    
    # @staticmethod
    # def handle_old_row(table: 'pd.DataFrame', old_row: 'pd.Series', index: int, new_lineid: int):
    #     table.loc[index, :] = old_row[:]
    #     table.loc[index, 'in_use'] = 'N'
    #     table.loc[index, 'superseded_by'] = new_lineid
    #     return table
