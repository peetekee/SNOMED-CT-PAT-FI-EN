import pandas as pd
import numpy as np
from services import Get, Database, Excel, Verhoeff
from actions import Inactivate, New, FSN, NewConcept
from config import Config


class Main:
    """The main driver class for the application

    This class is responsible for orchestrating the entire application. It reads the excel and database tables,
    determines the type of updates required, and then applies the updates to the database table. Finally, it writes
    the updated database table to the excel file.
    """
    def __init__(self) -> None:
        self.__config = Config()
        self.__excel = Excel(self.__config)
        self.__database = Database(self.__config)

    def __get_tables(self) -> tuple:
        """Reads the excel and database tables

        Returns:
            tuple: A tuple containing the excel and database tables in dataframes
        """
        excel = self.__excel.get()
        database = self.__database.get()
        return excel, database

    def __get_update_types(self, excel: 'pd.DataFrame', database: 'pd.DataFrame') -> tuple:
        """Determines the type of updates required

        Args:
            excel (pd.DataFrame): The excel containing the updates
            database (pd.DataFrame): The database table

        Returns:
            tuple: holds all the different types of updates required
        """
        edit_rows = Get.edit_rows(excel, database)
        new_rows = Get.new_rows(excel)
        fsn_rows = Get.fsn_rows(excel)
        inactivated_rows = Get.inactivated_rows(excel)
        activated_rows = Get.activated_rows(excel)
        return edit_rows, new_rows, fsn_rows, inactivated_rows, activated_rows

    def run(self):
        """The main driver function for the application
        """
        excel, database = self.__get_tables()
        edit_rows, new_rows, fsn_rows, inactivated_rows, activated_rows = self.__get_update_types(
            excel, database)

        # table = Inactivate(database, inactivated_rows).commit()
        # table = FSN(database, fsn_rows).commit()
        # table = New(database, new_rows).commit()
        table = NewConcept(database, edit_rows["new_concept"], self.__config).commit()
        self.__excel.post(table)
        # print(self.__excel.post(table))
        # table = self.__handle_updated_rows(edit_rows, database)
        # table = self.__handle_inactivated_rows(inactivated_rows, table)
        # table = self.__handle_new_rows(new_rows, table)
        # table = self.__component.empty_status_column(table)
        # self.__component.to_excel(table)
