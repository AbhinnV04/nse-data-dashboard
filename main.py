import requests
from requests.exceptions import HTTPError
import pandas as pd
from datetime import datetime
import time
import csv
import os
import sys

def print_hr():
    print("|".rjust(70, "-"))

def FetchOptionChainFromNSE(symbol: str, index: bool, session: requests.Session, headers: dict) -> dict | None:
    try:
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}" if index else f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Ensure we raise an exception for HTTP errors
        return response.json().get('records', {})
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred during data fetching: {err}")
    return None

def GetOptionChainCEData(option_chain_data_df: pd.DataFrame) -> pd.DataFrame:
    option_chain_ce = pd.DataFrame()
    option_chain_ce['CE'] = option_chain_data_df['CE']
    return pd.concat([option_chain_ce.drop('CE', axis=1), option_chain_ce['CE'].apply(pd.Series)], axis=1)

def GetOptionChainPEData(option_chain_data_df: pd.DataFrame) -> pd.DataFrame:
    option_chain_pe = pd.DataFrame()
    option_chain_pe['PE'] = option_chain_data_df['PE']
    return pd.concat([option_chain_pe.drop('PE', axis=1), option_chain_pe['PE'].apply(pd.Series)], axis=1)

def round_features(df: pd.DataFrame, decimal_places: int = 2) -> pd.DataFrame:
    numeric_columns = df.select_dtypes(include='number').columns
    df[numeric_columns] = df[numeric_columns].round(decimal_places)
    return df

def GetFeatures(df: pd.DataFrame, src_data: pd.DataFrame, underlying_value: float) -> pd.DataFrame:
    ce_data = GetOptionChainCEData(src_data)
    pe_data = GetOptionChainPEData(src_data)
    
    df["CE_OI"] = ce_data['openInterest']
    df["CE_CHNG_IN_OI"] = ce_data['changeinOpenInterest']
    df["CE_VOLUME"] = ce_data['totalTradedVolume']
    df["CE_IV"] = ce_data["impliedVolatility"]
    df["CE_LTP"] = ce_data["lastPrice"]
    df["CE_CHNG"] = ce_data["change"]
    df["CE_BID_QTY"] = ce_data["bidQty"]
    df["CE_BID_PRICE"] = ce_data['bidprice']
    df["CE_ASK_QTY"] = ce_data['askQty']
    df["CE_ASK_PRICE"] = ce_data['askPrice']
    
    df["strikePrice"] = src_data['strikePrice']
    
    df["PE_OI"] = pe_data['openInterest']
    df["PE_CHNG_IN_OI"] = pe_data['changeinOpenInterest']
    df["PE_VOLUME"] = pe_data['totalTradedVolume']
    df["PE_IV"] = pe_data["impliedVolatility"]
    df["PE_LTP"] = pe_data["lastPrice"]
    df["PE_CHNG"] = pe_data["change"]
    df["PE_BID_QTY"] = pe_data["bidQty"]
    df["PE_BID_PRICE"] = pe_data['bidprice']
    df["PE_ASK_QTY"] = pe_data['askQty']
    df["PE_ASK_PRICE"] = pe_data['askPrice']
    
    df["underlyingValue"] = underlying_value
    
    return round_features(df)  # Round the features before returning

def GetExpiryDates(symbol: str, index: bool, session: requests.Session, headers: dict) -> list:
    option_chain_record = FetchOptionChainFromNSE(symbol=symbol, index=index, session=session, headers=headers)
    response = option_chain_record.get('expiryDates', [])
    if response:
        return response  
    else:
        print("Failed to fetch expiry dates")
        return ["14-Aug-2024"]

def GetOptionChain(symbol: str, expiry: str, index: bool, session: requests.Session, headers: dict) -> pd.DataFrame:
    option_chain_record = FetchOptionChainFromNSE(symbol=symbol, index=index, session=session, headers=headers)
    option_chain_data = option_chain_record.get('data', [])
    option_chain_data_df = pd.DataFrame(option_chain_data)
    option_chain_data_df = option_chain_data_df[option_chain_data_df.expiryDate == expiry]

    option_chain = pd.DataFrame()
    underlying_value = option_chain_record.get('underlyingValue', 0.0)
    return GetFeatures(df=option_chain, src_data=option_chain_data_df, underlying_value=underlying_value)

def write_to_csv(data: pd.DataFrame, file_path: str, columns: list) -> None:
    file_exists = os.path.exists(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        if not file_exists:
            writer.writeheader()
        for _, row in data.iterrows():
            writer.writerow(row[columns].to_dict())

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
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
    
    while True:
        try:
            run(file_path, symbol, index, expiry, columns, session, headers)
            time.sleep(120)
        except KeyboardInterrupt:
            print("Process interrupted by user.")
            sys.exit()
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    main()
