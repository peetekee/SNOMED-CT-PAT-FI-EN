import pandas as pd


def clean_spaces(df: pd.DataFrame, codeid_column: list = ['CodeId', 'A:KorvaavaKoodi', 'ParentId']) -> pd.DataFrame:
    # # Filter columns, excluding the specified codeid column
    # columns_to_clean = [col for col in df.columns if not col in codeid_column]

    # for col in columns_to_clean:
    #     # Remove leading and trailing spaces
    #     df[col] = df[col].str.strip()
    #     # Replace double or multiple spaces with a single space
    #     df[col] = df[col].str.replace(r'\s{2,}', ' ', regex=True)

    return df