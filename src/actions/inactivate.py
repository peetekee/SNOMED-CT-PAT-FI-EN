import pandas as pd
from services.components import Get, Put


class Inactivate:
    # remember the lang rows
    def __handle_inactivated_rows(self, inactivated_rows: 'pd.DataFrame', database: 'pd.DataFrame'):
        for index, row in inactivated_rows.iterrows():
            index = Get.index_by_codeid(
                database, row["lineid"])
            database = Put.handle_inactivated_row(
                database, row, index)
        return database
