import requests
import time
import pandas as pd

def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        'user-agent': 'Mozilla/5.0',
        'accept-language': 'en',
        'accept-encoding': 'gzip, deflate, br'
    })
    return session

def fetch_data(url: str, session: requests.Session, retries: int = 5) -> dict:
    for attempt in range(retries):
        try:
            response = session.get(url)
            response.raise_for_status()
            return response.json()  # Convert response to JSON
        except requests.RequestException as e:
            if attempt < retries - 1:
                time.sleep(1)  # Wait before retrying
                continue
            else:
                raise e

def fetch_option_chain(symbol: str) -> (pd.DataFrame, list):
    session = create_session()
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}" 
    try:
        data = fetch_data(url, session)
        expiry_dates = data.get('records', {}).get('expiryDates', [])
        option_chain_data = data.get('records', {}).get('data', [])
        option_chain_df = pd.DataFrame(option_chain_data)
        return option_chain_df, expiry_dates[:3]  # Returning only 3 options for expiry dates
    except Exception as e:
        print(f"Error fetching option chain data: {e}")
        return pd.DataFrame(), ["14-Aug-2099"]  # Default date in case of error

