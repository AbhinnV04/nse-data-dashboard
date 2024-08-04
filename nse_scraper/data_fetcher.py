import requests
from requests.exceptions import HTTPError
import logging

def FetchOptionChainFromNSE(symbol, index, session, headers):
    try:
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}" if index else f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('records', {})
    except HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred during data fetching: {err}")
    return None

def GetExpiryDates(symbol, index, session, headers):
    option_chain_record = FetchOptionChainFromNSE(symbol=symbol, index=index, session=session, headers=headers)
    response = option_chain_record.get('expiryDates', [])
    if response:
        return response
    else:
        logging.warning("Failed to fetch expiry dates")
        return []
