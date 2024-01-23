import pandas as pd


class Excel:
    def __init__(self, config) -> None:
        self.__config = config

    def get(self):
        return pd.read_excel(self.__config.excel_path, engine="openpyxl", dtype=str, sheet_name=self.__config.excel_sheet)

    def post(self, table: 'pd.DataFrame'):
        table[["lineid", "sct_conceptid", "sct_termid", "sct_termid_en"]] = table[[
            "lineid", "sct_conceptid", "sct_termid", "sct_termid_en"]].astype(str)
        table = table.sort_values(
            by=["legacy_conceptid", "sct_termid_en", "lang"])
        table.to_excel(self.__config.output_file, index=False)
