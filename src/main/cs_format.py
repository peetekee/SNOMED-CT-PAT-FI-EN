import re
import os
from numpy import nan
from services import Database
from config import Config, COLUMNS


class CSFormat:
    def __init__(self, password: str):
        self.__config = Config(password)
        self.__db = Database(self.__config)

    def __qui_category(self, row):
        if row[COLUMNS["tmdc"]][0] in ["A", "D", "M"]:
            return "diagnosis"
        elif row[COLUMNS["tmdc"]][0] == "C":
            return "cytology"
        elif row[COLUMNS["tmdc"]][0] == "T":
            return "topography"
        else:
            return "unknown"

    def __concept_category(self, row):
        match = re.search(
            "(?P<category>\(([^()]*)\))$", row[COLUMNS["concept_fsn"]])
        if match and match.group("category"):
            return match.group("category")[1:-1]
        return "unknown"

    def __short_term(self, row):
        return row[COLUMNS["term"]][:50] if len(row[COLUMNS["term"]]) > 50 else row[COLUMNS["term"]]

    def __hierarchy_level(self, row):
        return 0 if row[COLUMNS["lang"]] == "en" else 1

    def __cs_columns(self, df):
        df["hierarchy_level"] = df.apply(self.__hierarchy_level, axis=1)
        df["gui_category"] = df.apply(self.__qui_category, axis=1)
        df["concept_category"] = df.apply(self.__concept_category, axis=1)
        df["short_name"] = df.apply(self.__short_term, axis=1)
        df["abbreviation"] = df.apply(self.__short_term, axis=1)
        df["order_number"] = None
        return df

    def __select_columns(self, df):    
        df = df[[
            COLUMNS["code_id"],
            "gui_category",
            COLUMNS["lang"],
            COLUMNS["active"],
            COLUMNS["legacy_concept_id"],
            COLUMNS["legacy_term_id"],
            COLUMNS["concept_id"],
            COLUMNS["concept_fsn"],
            "concept_category",
            COLUMNS["term_id"],
            COLUMNS["en_row_code_id"],
            COLUMNS["term"],
            COLUMNS["icdo_morfologia"],
            COLUMNS["beginning_date"],
            COLUMNS["expiring_date"],
            COLUMNS["korvaava_koodi"],
            COLUMNS["inaktivoinnin_selite"],
            "order_number",
            "abbreviation",
            "short_name",
            "hierarchy_level"
        ]]
        return df

    def __rename_columns(self, df):
        df = df.rename(columns={
            "abbreviation": "Abbreviation",
            "short_name": "ShortName",
            "hierarchy_level": "HierarchyLevel",
            "concept_category": "A:Concept_Category",
            "gui_category": "A:GUI_Category",
            "order_number": "ANUM:JarjestysNro"
        })
        return df

    def __sort_df(self, df):
        df = df.sort_values(by=["A:Legacy_ConceptID", "ParentId", "A:Lang"])
        df["ANUM:JarjestysNro"] = range(1, 1 + len(df))
        df["ANUM:JarjestysNro"] = df["ANUM:JarjestysNro"].astype(int)
        return df

    def __parent_id(self, row):
        return None if row["A:Lang"] == "en" else row["ParentId"]

    def __to_excel(self, final_df):
        dirname = os.path.dirname(__file__)
        excel_path = os.path.join(dirname, self.__config.output_file_path, self.__config.cs_table)
        final_df.replace('None', nan, inplace=True)
        final_df.to_excel(excel_path, index=False)

    def run(self, progress_callback=None):
        if progress_callback:
            progress_callback(5)
        df = self.__db.get()
        if progress_callback:
            progress_callback(10)
        df = self.__cs_columns(df)
        if progress_callback:
            progress_callback(20)
        df = self.__select_columns(df)
        if progress_callback:
            progress_callback(30)
        df = self.__rename_columns(df)
        if progress_callback:
            progress_callback(40)
        df = self.__sort_df(df)
        if progress_callback:
            progress_callback(50)
        df[COLUMNS["en_row_code_id"]] = df.apply(self.__parent_id, axis=1)
        if progress_callback:
            progress_callback(80)
        self.__to_excel(df)
        if progress_callback:
            progress_callback(100)
