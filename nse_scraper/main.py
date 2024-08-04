# nse_scraper/main.py
from datetime import datetime
import os
import pandas as pd
import requests
import time
import sys
import csv

from data_fetcher import FetchOptionChainFromNSE
from data_processor import GetFeatures
from utils import print_hr, write_to_csv, initialize_csv_file


def GetExpiryDates(symbol: str, index: bool, session: requests.Session, headers: dict) -> list:
    option_chain_record = FetchOptionChainFromNSE(symbol=symbol, index=index, session=session, headers=headers)
    response = option_chain_record.get('expiryDates', [])
    if response:
        return response  
    else:
        print("Failed to fetch expiry dates")
        return ["14-Aug-2024"] # change return value here

def GetOptionChain(symbol: str, expiry: str, index: bool, session: requests.Session, headers: dict) -> pd.DataFrame:
    option_chain_record = FetchOptionChainFromNSE(symbol=symbol, index=index, session=session, headers=headers)
    option_chain_data = option_chain_record.get('data', [])
    option_chain_data_df = pd.DataFrame(option_chain_data)
    option_chain_data_df = option_chain_data_df[option_chain_data_df.expiryDate == expiry]

    option_chain = pd.DataFrame()
    underlying_value = option_chain_record.get('underlyingValue', 0.0)
    return GetFeatures(df=option_chain, src_data=option_chain_data_df, underlying_value=underlying_value)


def run(file_path: str, symbol: str, index: bool, expiry: str, columns: list, session: requests.Session, headers: dict) -> None:
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print_hr()
    print(f"Fetching data at: {time_now}\n")
    
    OptionChain_NIFTY = GetOptionChain(symbol=symbol, expiry=expiry, index=index, session=session, headers=headers)
    OptionChain_NIFTY['TimeStamp'] = time_now
    print("Updating CSV...")
    write_to_csv(OptionChain_NIFTY, file_path, columns)
    print_hr()
    print()

def main():
    session = requests.Session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'accept-language': 'en,gu;q=0.9,hi;q=0.8',
        'accept-encoding': 'gzip, deflate, br'
    }
    
    response = session.get("https://www.nseindia.com/", headers=headers)
    if response.status_code == 200:
        print_hr()
        print("Session Status Code 200: OK\nSafe to Proceed!")
        print_hr()
    else:
        print_hr()
        print(f"Status Code {response.status_code}")
        print("Exiting...")
        sys.exit()
    
    symbol = "NIFTY"
    index = True  # Nifty is an index
    expiry = GetExpiryDates(symbol, index, session, headers)[0]
    file_path = f"{symbol}_data.csv"
    
    columns = [
        'CE_OI', 'CE_CHNG_IN_OI', 'CE_VOLUME', 'CE_IV', 'CE_LTP', 'CE_CHNG',
        'CE_BID_QTY', 'CE_BID_PRICE', 'CE_ASK_QTY', 'CE_ASK_PRICE',
        'strikePrice', 'PE_OI', 'PE_CHNG_IN_OI', 'PE_VOLUME', 'PE_IV', 'PE_LTP',
        'PE_CHNG', 'PE_BID_QTY', 'PE_BID_PRICE', 'PE_ASK_QTY', 'PE_ASK_PRICE',
        'underlyingValue', 'TimeStamp'
    ]

    if not os.path.exists(file_path):
        initialize_csv_file()

    while True:
        try:
            run(file_path, symbol, index, expiry, columns, session, headers)
            print("Waiting")
            time.sleep(120)  # Change in app
        except KeyboardInterrupt:
            print("Process interrupted by user.")
            sys.exit()
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    main()
