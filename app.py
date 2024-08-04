import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

from nse_scraper import FetchOptionChainFromNSE, GetFeatures, write_to_csv, initialize_csv_file, GetExpiryDates, create_session, fetch_page

# Function to fetch the NSE home page to ensure the server is reachable
def check_server(session: requests.Session):
    try:
        response = fetch_page("https://www.nseindia.com/", session)
        if response.status_code == 200:
            pass
        else:
            st.write(f"Server returned status code {response.status_code}.")
    except Exception as e:
        st.write(f"Error checking server: {e}")

def get_symbol_names(symbol_type: str):
    if symbol_type == "Index":
        return ["NIFTY", "BANKNIFTY", "FINNIFTY", "NIFTYNXT50", "MIDCNIFTY"]
    else:
        return ["RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK"]

def export_data(data: pd.DataFrame, file_format: str, symbol: str):
    if file_format == "csv":
        file_name = f"{symbol}_Data.csv"
        data.to_csv(file_name, index=False)
        return file_name
    elif file_format == "pdf":
        st.write("PDF export is not yet implemented.")
        return None

st.title("NSE Data Dashboard")

with st.sidebar:
    st.header("Choose an Index/Symbol")
    
    symbol_type = st.radio('Symbol Type', ['Index', 'Stock'])
    symbol_names = get_symbol_names(symbol_type)
    symbol = st.selectbox('Symbol Name', symbol_names)

    st.header("Filters")
    session = create_session()
    check_server(session)  # Ensure the server is reachable
    
    valid_expiry_dates = GetExpiryDates(symbol=symbol, index=(symbol_type == "Index"), session=session, headers=session.headers)
    expiry_date = st.selectbox('Expiry Date', valid_expiry_dates)

    valid_strike_price = [25000, 25500, 26000, 26500, 27000]
    strike_prices = st.multiselect('Strike Price', valid_strike_price, default=valid_strike_price[:1])
    
    time_delays = ["1 Min", "3 Min", "5 Min"]
    time_delay = st.radio("Time Delay", time_delays)

# Placeholder for DataFrame
df = pd.DataFrame()  # You should replace this with actual data fetching and processing

# Displaying the selected values for debugging
st.write(f"Selected Symbol: {symbol}")
st.write(f"Selected Expiry Date: {expiry_date}")
st.write(f"Selected Strike Prices: {strike_prices}")
