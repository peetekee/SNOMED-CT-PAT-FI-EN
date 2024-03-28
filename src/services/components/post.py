import pandas as pd


class Post:
    """Includes post methods that add something

    Used by the actions to add rows to the database.
    """

    @staticmethod
    def new_row_to_database_table(new_row: 'pd.Series', database: 'pd.DataFrame') -> 'pd.DataFrame':
        """Adds a new row to the database

        Args:
            new_row (pd.Series): the new row to be added
            database (pd.DataFrame): the database

        Returns:
            pd.DataFrame: the updated database
        """
        database = pd.concat(
            [database, new_row.to_frame().T], ignore_index=True)
        return database
