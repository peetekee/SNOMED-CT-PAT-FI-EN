import os
import pandas as pd
import sqlalchemy as db
import psycopg2
from datetime import datetime
from config import COLUMNS


class Database:
    """Class for the database interaction

    Reads and writes data to the database.
    """

    def __init__(self, config) -> None:
        self.__engine = config.connection
        self.__schema = config.schema
        self.__intl_schema = config.intl_schema
        self.__table_name = config.table
        self.__output_table = config.output_table
        self.__database = config.database
        self.__username = config.username
        self.__password = config.password
        self.__connection_address = config.connection_address
        self.__intl_tables = ["snap_concept", "snap_description", "snap_attributevaluerefset", "snap_historical_refset", "snap_pref", "snap_fsn"]
        self.__view_file = os.path.join(os.path.dirname(__file__), "../../intl/create_snap_views.sql")

    def get(self) -> 'pd.DataFrame':
        """Read the table defined in the config file

        Connection parameters are defined in the config file as well.

        Read the columns as type string and the code_id as type int.
        Previously the automatic type conversion was used, but it caused problems.

        Returns:
            pd.DataFrame: The database table
        """

        try:
            with self.__engine.connect() as connection:
                query = db.text(
                    f"SELECT * FROM {self.__schema}.{self.__table_name}")

                df = pd.read_sql(query, connection)
                df = df.astype(str)
                df[COLUMNS["code_id"]] = df[COLUMNS["code_id"]].astype(int)
                return df
        except Exception as e:
            print('Error while reading data from database')
            print(e)

    def create_intl_views(self):
        # Connect to the PostgreSQL database using the credentials
        conn = psycopg2.connect(
            dbname=self.__database,
            user=self.__username,
            password=self.__password,
            host=self.__connection_address
        )
        cur = conn.cursor()

        # Iterate over all SQL files in the Views folder and execute them
        with open(self.__view_file, 'r') as file:
            sql_query = file.read()
            try:
                cur.execute(sql_query)
                conn.commit()
            except Exception as e:
                print(e)
        # Close the cursor and connection
        cur.close()
        conn.close()

    def get_intl(self):
        intl_tables = {}
        try:
            with self.__engine.connect() as connection:
                for table_name in self.__intl_tables:
                    query = db.text(
                        f"SELECT * FROM {self.__intl_schema}.{table_name}")
                    df = pd.read_sql(query, connection)
                    df = df.astype(str)
                    intl_tables[table_name] = df
                return intl_tables
        except Exception as e:
            print('Error while reading data from database')
            print(e)

    def post(self, df: 'pd.DataFrame') -> None:
        """Write the dataframe to the database

        Parameters and name of the table are defined in the config file.

        Args:
            df (pd.DataFrame): The dataframe to be written to the database
        """
        with self.__engine.connect() as connection:
            try:
                df.to_sql(self.__output_table, con=connection,
                          schema=self.__schema, index=False, if_exists='replace')
            except Exception:
                date = datetime.now()
                date = date.strftime('%Y%m%d_%H%M')
                table_name = f'sct_pat_fi_kanta_{date}'
                df.to_sql(table_name, con=connection, schema=self.__schema)
