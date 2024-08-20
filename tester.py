import pandas as pd
from sqlalchemy import create_engine

from data_fetcher.fetch_data import fetch_option_chain
from data_fetcher.data_processor import get_features
from data_fetcher.storage import insert_data_from_df


def test_create_and_insert(symbol):
    data, expiry = fetch_option_chain(symbol)
    data_processed = get_features(data)
    insert_data_from_df(data_processed, symbol)
    # print(data_processed.head(5))
        
def test_read(table_name):
    engine = create_engine('sqlite:///data.db')
    df = pd.read_sql_table(table_name, con=engine)
    #print(df.head(5))
    df.to_csv(f'output_{table_name}.csv', index=False)


if __name__ == '__main__':
    test_read('NIFTY')
    test_read('BANKNIFTY')
    test_read('FINNIFTY')