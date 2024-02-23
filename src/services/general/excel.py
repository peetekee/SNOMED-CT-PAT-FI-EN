import pandas as pd
from config import COLUMNS


class Excel:
    def __init__(self, config) -> None:
        self.__config = config

    def get(self):
        return pd.read_excel(self.__config.excel_path, engine="openpyxl", dtype=str, sheet_name=self.__config.excel_sheet)

    def post(self, table: 'pd.DataFrame'):
        table[[COLUMNS["code_id"], COLUMNS["concept_id"], COLUMNS["term_id"], COLUMNS["en_row_code_id"]]] = table[[
            COLUMNS["code_id"], COLUMNS["concept_id"], COLUMNS["term_id"], COLUMNS["en_row_code_id"]]].astype(str)
        table = table.sort_values(
            by=[COLUMNS["legacy_concept_id"], COLUMNS["en_row_code_id"], COLUMNS["lang"]])
        table.to_excel(self.__config.output_file, index=False)
