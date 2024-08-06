import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd

from nse_scraper import fetch_option_chain, get_features, get_column_names

# Example usage:
symbol = "NIFTY"
option_chain_df, expiry_dates = fetch_option_chain(symbol)
features_df = get_features(pd.DataFrame(), option_chain_df)
print(features_df[255:].head())
print(features_df["SPOT_PRICE"].value_counts())
print(get_column_names())
