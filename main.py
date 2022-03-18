import pandas as pd
from db.util import *


def main():
    df = pd.read_csv('DATA.csv')
    bulk_insert(df, 'sfl_data')


if __name__ == '__main__':
    main()
