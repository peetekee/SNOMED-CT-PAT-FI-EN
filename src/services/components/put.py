import pandas as pd


class Put:
    @staticmethod
    def handle_old_row(table: 'pd.DataFrame', old_row: 'pd.Series', index: int, new_lineid: int):
        table.loc[index, :] = old_row[:]
        table.loc[index, 'in_use'] = 'N'
        table.loc[index, 'superseded_by'] = new_lineid
        return table

    @staticmethod
    def handle_new_row(table: 'pd.DataFrame', new_row: int, new_lineid: int):
        new_row['lineid'] = new_lineid
        new_row['in_use'] = 'Y'
        new_row = new_row.to_frame().T
        return pd.concat([table, new_row], ignore_index=True)

    @staticmethod
    def handle_inactivated_row(table: 'pd.DataFrame', inactivated_row: 'pd.Series', index: int):
        table.loc[index, 'in_use'] = 'N'
        table.loc[index, 'supersededtime'] = inactivated_row['supersededtime']
        table.loc[index, 'inaktivoinnin_selite'] = inactivated_row['inaktivoinnin_selite']
        return table

    @staticmethod
    def handle_activated_row(table: 'pd.DataFrame', activated_row: 'pd.Series', index: int):
        table.loc[index, 'in_use'] = 'Y'
        table.loc[index, 'effectivetime'] = activated_row['effectivetime']
        table.loc[index, 'supersededtime'] = activated_row['supersededtime']
        table.loc[index, 'inaktivoinnin_selite'] = None
        return table
