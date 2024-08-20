import requests
import time
import pandas as pd

def create_session() -> requests.Session:
    """Create a session with custom headers."""
    session = requests.Session()
    session.headers.update({
        'user-agent': 'Mozilla/5.0',
        'accept-language': 'en',
        'accept-encoding': 'gzip, deflate, br'
    })
    return session

def fetch_data(url: str, session: requests.Session, retries: int = 5) -> dict:
    """Fetch data from the URL with retry logic."""
    delay = 1
    for attempt in range(retries):
        try:
            response = session.get(url)
            response.raise_for_status()
            return response.json()  
        except requests.RequestException as e:
            if attempt < retries - 1:
                # print(f"Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
                delay *= 2  # Exponential backoff
            else:
                print(f"Failed after {retries} attempts: {e}")
                return {}  # Return empty dict on failure


def fetch_option_chain(symbol: str) -> (pd.DataFrame, list):
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}" 
    
    try:
        session = create_session()
        data = fetch_data(url, session)
        expiry_dates = data.get('records', {}).get('expiryDates', [])
        option_chain_data = data.get('records', {}).get('data', [])
        
        if option_chain_data:
            option_chain_df = pd.DataFrame(option_chain_data)
        else:
            print(f"\n\tNo option chain data available for symbol: {symbol}\nFailed fetching returning empty!:")
            option_chain_df = pd.DataFrame()  # Return empty DataFrame if no data
        
        return option_chain_df, expiry_dates
    
    except Exception as e:
        print(f"Error fetching option chain data for {symbol}: {e}")
        return pd.DataFrame(), []  # Return empty DataFrame and list on error
