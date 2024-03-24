import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from numpy import nan

COLUMNS = {
    "code_id": "CodeId",
    "status": "status",
    "tmdc": "tmdc",
    "lang": "A:Lang",
    "active": "A:Active",
    "legacy_concept_id": "A:Legacy_ConceptID",
    "legacy_term_id": "A:Legacy_TermID",
    "tays_snomed_ii": "tays_snomed_ii",
    "concept_id": "A:SNOMEDCT",
    "concept_fsn": "A:SCT_Concept_FSN",
    "term_id": "A:SCT_TermID",
    "en_row_code_id": "ParentId",
    "term": "LongName",
    "parent_concept_id": "parent_conceptid",
    "parent_concept_fsn": "parent_concept_fsn",
    "edit_comment": "edit_comment",
    "icdo_morfologia": "A:ICD-O-3_Morfologia",
    "icdo_term": "icdo_term",
    "icdo_synonyms": "icdo_synonyms",
    "beginning_date": "BeginningDate",
    "expiring_date": "ExpiringDate",
    "korvaava_koodi": "A:KorvaavaKoodi",
    "inaktivoinnin_selite": "A:InaktivoinninSelite",
    "sn2_code": "sn2_code",
    "sn2_term": "sn2_term",
    "endo": "endo",
    "gastro": "gastro",
    "gyne": "gyne",
    "iho": "iho",
    "hema": "hema",
    "keuhko": "keuhko",
    "nefro": "nefro",
    "neuro": "neuro",
    "paa_kaula": "paa_kaula",
    "pedi": "pedi",
    "pehmyt": "pehmyt",
    "rinta": "rinta",
    "syto": "syto",
    "uro": "uro",
    "verenkierto_yleiset": "verenkierto_yleiset"
}

EDIT_TYPES = ["new_concept", "new_term", "nationalize_concept", "nationalize_term"]

COPY_COLUMNS = [
        COLUMNS["tmdc"],
        COLUMNS["lang"],
        COLUMNS["tays_snomed_ii"],
        COLUMNS["parent_concept_id"],
        COLUMNS["parent_concept_fsn"],
        COLUMNS["icdo_term"],
        COLUMNS["icdo_synonyms"],
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
        COLUMNS["verenkierto_yleiset"]
    ]



class Config:
    """Class for configuration

    Includes basic configuration for the application
    Includes database connection, schema, table, excel file, excel sheet, output file and output table

    Attributes:
        __database_connection (sqlalchemy.engine.base.Engine): Database connection
        __database_schema (str): Database schema
        __table_name (str): Table name
        __excel_path (str): Excel file path
        __excel_sheet (str): Excel sheet name
        __output_file (str): Output file path
        __output_table (str): Output table name

    Class variables:
        columns (dict): Keys are the column names used in the application and
                        values are the column names in the database.
    """


    def __init__(self):
        self.__database_connection = None
        self.__database_schema = None
        self.__table_name = None
        self.__excel_path = None
        self.__excel_sheet = None
        self.__output_file = None
        self.__output_table = None
        self.__version_date = None
        self.__default_expiring_date = None
        self.__langs = ["fi", "sv"]
        self.__empty_values = [None, "", nan]
        self.__initialize()

    @property
    def connection(self):
        return self.__database_connection

    @property
    def schema(self):
        return self.__database_schema

    @property
    def table(self):
        return self.__table_name

    @property
    def excel_path(self):
        return self.__excel_path

    @property
    def excel_sheet(self):
        return self.__excel_sheet

    @property
    def output_file(self):
        return self.__output_file

    @property
    def output_table(self):
        return self.__output_table
    
    @property
    def version_date(self):
        return self.__version_date
    
    @property
    def default_expiring_date(self):
        return self.__default_expiring_date
    
    @property
    def langs(self):
        return self.__langs
    
    @property
    def empty_values(self):
        return self.__empty_values

    def __initialize(self):
        dirname = os.path.dirname(__file__)
        try:
            load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
        except FileNotFoundError:
            print("No .env file found\nWrite .env file with the following variables:\n")
            print(r"\nCONNECTION = <username;password@connection_address/database>\n")
            print(r"SCHEMA = <schema_name>\n")

        self.__database_connection = create_engine(os.getenv("CONNECTION"))
        self.__database_schema = os.getenv("SCHEMA")
        self.__table_name = os.getenv("TABLE")
        file_name = os.getenv("EXCEL_FILE")
        self.__excel_path = os.path.join(dirname, "..", file_name)
        self.__excel_sheet = os.getenv("EXCEL_SHEET")
        output_file_name = os.getenv("OUTPUT_FILE")
        self.__output_file = os.path.join(dirname, "..", output_file_name)
        self.__output_table = os.getenv("OUTPUT_TABLE")
        self.__version_date = str(os.getenv("DATE"))
        self.__default_expiring_date = str(os.getenv("DEFAULT_EXPIRING_DATE"))
