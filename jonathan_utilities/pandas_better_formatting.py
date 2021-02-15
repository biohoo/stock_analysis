import pandas as pd

def set_pandas_options():
    pd.set_option('display.max_columns', None)  # or 1000
    pd.set_option('display.max_rows', None)  # or 1000
    pd.set_option('display.max_colwidth', None)  # or 199


if __name__ == '__main__':
    set_pandas_options()