import pandas as pd


class Row:
    def __init__(self, type, new_row, old_row, lang_rows) -> None:
        self.__type = type
        self.__old_row = None
        self.__new_row = None
        self.__lang_rows = None


    @property
    def new_row(self) -> 'pd.Series':
        return self.__new_row
    
    @property
    def old_row(self) -> 'pd.Series':
        return self.__old_row
    
    @property
    def lang_rows(self) -> 'pd.DataFrame':
        return self.__lang_rows
    
    def __set_up(self, old_row:'pd.Series', new_row:'pd.Series', lang_rows:'pd.DataFrame'):
        self.__old_row = old_row
        self.__new_row = new_row
        self.__lang_rows = lang_rows
    

    


    


