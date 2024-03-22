import pandas as pd
import sqlalchemy as db
from datetime import datetime
from config import COLUMNS


class Database:
    def __init__(self, config) -> None:
        self.__engine = config.connection
        self.__schema = config.schema
        self.__table_name = config.table
        self.__output_table = config.output_table

    def get(self) -> 'pd.DataFrame':
        try:
            with self.__engine.connect() as connection:
                query = db.text(f"SELECT * FROM {self.__schema}.{self.__table_name}")

                df = pd.read_sql(query, connection)
                df = df.astype(str)
                df[COLUMNS["code_id"]] = df[COLUMNS["code_id"]].astype(int)
                return df
        except Exception as e:
            print('Error while reading data from database')
            print(e)

    def post(self, df: 'pd.DataFrame') -> None:
        with self.__engine.connect() as connection:
            try:
                df.to_sql(self.__output_table, con=connection,
                          schema=self.__schema)
            except Exception:
                date = datetime.now()
                date = date.strftime('%Y%m%d_%H%M')
                table_name = f'sct_pat_fi_kanta_{date}'
                df.to_sql(table_name, con=connection, schema=self.__schema)
                