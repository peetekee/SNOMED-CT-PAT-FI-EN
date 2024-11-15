import pandas as pd
from numpy import nan
from config import COLUMNS


class Excel:
    """Class for interacting with Excel files

    The excel files contain the updates made by the pathologists.
    """

    def __init__(self, config) -> None:
        self.__config = config

    def get(self) -> 'pd.DataFrame':
        """Read the excel file

        The excel file is defined in the environment variables.

        Returns:
            pd.DataFrame: The update excel file
        """

        excel = pd.read_excel(self.__config.excel_path, engine="openpyxl",
                              dtype=str, sheet_name=self.__config.excel_sheet)
        return excel

    def post(self, table: 'pd.DataFrame') -> None:
        """Write the table to the excel file

        The excel file is defined in the environment variables.
        The columns are mapped to the correct names.
        Args:
            table (pd.DataFrame): The table to be written to the excel file
        """
        
        table[[COLUMNS["code_id"], COLUMNS["concept_id"], COLUMNS["term_id"], COLUMNS["en_row_code_id"]]] = table[[
            COLUMNS["code_id"], COLUMNS["concept_id"], COLUMNS["term_id"], COLUMNS["en_row_code_id"]]].astype(str)
        table = table.sort_values(
            by=[COLUMNS["legacy_concept_id"], COLUMNS["en_row_code_id"], COLUMNS["lang"]])
        table.replace('None', nan, inplace=True)
        table.to_excel(self.__config.output_file, index=False)

    def post_intl_comparison(self, table: 'pd.Dataframe'):
        mask = [
            COLUMNS["code_id"],
            "accept",
            "meta",
            COLUMNS["status"],
            COLUMNS["tmdc"],
            COLUMNS["lang"],
            COLUMNS["active"],
            COLUMNS["legacy_concept_id"],
            COLUMNS["legacy_term_id"],
            COLUMNS["tays_snomed_ii"],
            COLUMNS["concept_id"],
            COLUMNS["concept_fsn"],
            COLUMNS["term_id"],
            COLUMNS["en_row_code_id"],
            COLUMNS["term"],
            COLUMNS["parent_concept_id"],
            COLUMNS["parent_concept_fsn"],
            COLUMNS["edit_comment"],
            COLUMNS["icdo_morfologia"],
            COLUMNS["icdo_term"],
            COLUMNS["icdo_synonyms"],
            COLUMNS["beginning_date"],
            COLUMNS["expiring_date"],
            COLUMNS["korvaava_koodi"],
            COLUMNS["inaktivoinnin_selite"],
            COLUMNS["sn2_code"],
            COLUMNS["sn2_term"],
            COLUMNS["endo"],
            COLUMNS["gastro"],
            COLUMNS["gyne"],
            COLUMNS["iho"],
            COLUMNS["hema"],
            COLUMNS["keuhko"],
            COLUMNS["nefro"],
            COLUMNS["neuro"],
            COLUMNS["paa_kaula"],
            COLUMNS["pedi"],
            COLUMNS["pehmyt"],
            COLUMNS["rinta"],
            COLUMNS["syto"],
            COLUMNS["uro"],
            COLUMNS["verenkierto_yleiset"],
        ]
        
        table = table[mask]
        table = table.sort_values(
            by=[COLUMNS["code_id"], COLUMNS["status"]])
        table.replace('None', nan, inplace=True)
        table.to_excel(self.__config.intl_output_file, index=False)

    def post_check(self, table: 'pd.DataFrame') -> None:
        """Write the table to the excel file

        The excel file is defined in the environment variables.
        The columns are mapped to the correct names.
        Args:
            table (pd.DataFrame): The table to be written to the excel file
        """
        
        table[[COLUMNS["code_id"], COLUMNS["concept_id"], COLUMNS["term_id"], COLUMNS["en_row_code_id"]]] = table[[
            COLUMNS["code_id"], COLUMNS["concept_id"], COLUMNS["term_id"], COLUMNS["en_row_code_id"]]].astype(str)
        table = table.sort_values(
            by=["error_message",COLUMNS["legacy_concept_id"], COLUMNS["en_row_code_id"], COLUMNS["lang"]])
        table.replace('None', nan, inplace=True)
        table.to_excel(self.__config.output_file, index=False)
