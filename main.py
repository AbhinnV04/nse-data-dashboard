import requests
import pandas as pd
from datetime import datetime
import time
import sys
import os
import logging
from nse_scraper import FetchOptionChainFromNSE, GetExpiryDates, GetFeatures, GetColumnNames, write_to_csv


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def GetOptionChain(symbol, expiry, index, session, headers):
    option_chain_record = FetchOptionChainFromNSE(symbol=symbol, index=index, session=session, headers=headers)
    option_chain_data = option_chain_record.get('data', [])
    option_chain_data_df = pd.DataFrame(option_chain_data)
    option_chain_data_df = option_chain_data_df[option_chain_data_df.expiryDate == expiry]

    option_chain = pd.DataFrame()
    return GetFeatures(df=option_chain, src_data=option_chain_data_df)

def run(file_path, symbol, index, expiry, columns, session, headers):
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Fetching data at: {time_now}")

    OptionChain_NIFTY = GetOptionChain(symbol=symbol, expiry=expiry, index=index, session=session, headers=headers)
    OptionChain_NIFTY['TimeStamp'] = time_now
    logging.info("Updating CSV...")
    write_to_csv(OptionChain_NIFTY, file_path, columns)

def main():
    session = requests.Session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'accept-language': 'en,gu;q=0.9,hi;q=0.8',
        'accept-encoding': 'gzip, deflate, br'
    }

    response = session.get("https://www.nseindia.com/", headers=headers)
    if response.status_code == 200:
        logging.info("Session Status Code 200: OK. Safe to Proceed!")
    else:
        logging.error(f"Status Code {response.status_code}. Exiting...")
        sys.exit()

    symbol = "NIFTY"
    index = True  # Nifty is an index
    expiry = GetExpiryDates(symbol, index, session, headers)[0]
    file_path = f"{symbol}_data.csv"

    columns = GetColumnNames()

    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()

    while True:
        try:
            run(file_path, symbol, index, expiry, columns, session, headers)
            time.sleep(120)
        except KeyboardInterrupt:
            logging.info("Process interrupted by user.")
            sys.exit()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    main()
