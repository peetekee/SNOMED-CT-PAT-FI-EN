import pandas as pd
from config import COLUMNS, COPY_COLUMNS
from .get import Get


class Set:
    @staticmethod
    def en_row_code_id(en_row: 'pd.Series', database: 'pd.DataFrame') -> 'pd.Series':
        en_row[COLUMNS["code_id"]] = Get.next_codeid(database)
        en_row[COLUMNS["en_row_code_id"]] = en_row[COLUMNS["code_id"]]
        return en_row

    @staticmethod
    def date(row: 'pd.Series', config: object) -> 'pd.Series':
        row[COLUMNS["active"]] = "Y"
        row[COLUMNS["beginning_date"]] = config.version_date
        row[COLUMNS["expiring_date"]
            ] = config.default_expiring_date
        return row

    @staticmethod
    def administrative(new_row: 'pd.Series', old_row: 'pd.Series', config: object) -> 'pd.Series':
        for column in COPY_COLUMNS:
            if new_row[column] in config.empty_values:
                new_row[column] = old_row[column]
        return new_row
