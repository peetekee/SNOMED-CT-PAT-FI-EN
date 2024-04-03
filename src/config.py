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

EDIT_TYPES = ["new_concept", "new_term",
              "nationalize_concept", "nationalize_term"]

COPY_COLUMNS = [
    COLUMNS["tmdc"],
    COLUMNS["lang"],
    COLUMNS["tays_snomed_ii"],
    COLUMNS["parent_concept_id"],
    COLUMNS["parent_concept_fsn"],
    COLUMNS["icdo_morfologia"],
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

ADMINISTRATIVE_COLUMNS = [
    COLUMNS["tays_snomed_ii"],
    COLUMNS["parent_concept_id"],
    COLUMNS["parent_concept_fsn"],
    COLUMNS["edit_comment"],
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
    COLUMNS["verenkierto_yleiset"],
]


class Config:
    """Class for configuration

    Includes basic configuration for the application
    The services and actions classes use this class to get the configuration values.
    It reads the configuration values from the .env file and initializes the class variables.

    Attributes:
        __database_connection (sqlalchemy.engine.base.Engine): Database connection
        __database_schema (str): Database schema
        __table_name (str): Table name
        __excel_path (str): Excel file path
        __excel_sheet (str): Excel sheet name
        __output_file (str): Output file path
        __output_table (str): Output table name
        __version_date (str): Version date
        __default_expiring_date (str): Default expiring date
        __langs (list): List of languages
        __empty_values (list): List of empty values
    """

    def __init__(self, password):
        self.__password = password
        self.__database_connection = None
        self.__database_schema = None
        self.__table_name = None
        self.__excel_path = None
        self.__excel_sheet = None
        self.__output_file = None
        self.__output_file_path = None
        self.__output_table = None
        self.__version_date = None
        self.__default_expiring_date = None
        self.__langs = ["fi", "sv"]
        self.__empty_values = [None, "", nan]
        self.__cs_table = None
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
    def output_file_path(self):
        return self.__output_file_path

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
    
    @property
    def cs_table(self):
        return self.__cs_table

    def __initialize(self):
        dirname = os.path.dirname(__file__)
        try:
            load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
        except FileNotFoundError:
            print("No .env file found\nWrite .env file with the following variables:\n")
            print(r"\nCONNECTION = <username;password@connection_address/database>\n")
            print(r"SCHEMA = <schema_name>\n")
        self.__database_schema = os.getenv("SCHEMA")
        self.__table_name = os.getenv("TABLE")
        self.__excel_path = os.getenv("EXCEL_FILE")
        print(self.__excel_path)
        self.__excel_sheet = os.getenv("EXCEL_SHEET")
        self.__output_file = os.getenv("OUTPUT_FILE")
        self.__output_table = os.getenv("OUTPUT_TABLE")
        self.__version_date = str(os.getenv("DATE"))
        self.__default_expiring_date = str(os.getenv("DEFAULT_EXPIRING_DATE"))
        connection = f"postgresql://{os.getenv('USERNAME')}:{self.__password}@{os.getenv('CONNECTION_ADDRESS')}:{os.getenv('PORT')}/{os.getenv('DATABASE')}"
        self.__database_connection = create_engine(connection)
        self.__cs_table = os.getenv("CS_TABLE")
