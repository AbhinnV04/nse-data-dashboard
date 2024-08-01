# nse_scraper/data_fetcher.py
import requests
from requests.exceptions import HTTPError

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