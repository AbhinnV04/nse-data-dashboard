import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import nse_scraper
from nse_scraper import fetch_option_chain
import pandas as pd


def test_fetch_option_chain():
    symbol = "NIFTY"
    option_chain_df, expiry_dates = fetch_option_chain(symbol)
    
    # Printing the results
    print("Expiry Dates:", expiry_dates)
    print(option_chain_df.head())
    
    # Basic assertions (modify as needed)
    assert isinstance(option_chain_df, pd.DataFrame), "Expected DataFrame"
    assert isinstance(expiry_dates, list), "Expected list of expiry dates"
    assert len(expiry_dates) > 0, "Expiry dates list should not be empty"

if __name__ == "__main__":
    test_fetch_option_chain()
