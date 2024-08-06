import streamlit as st
import pandas as pd
import time
from nse_scraper import fetch_option_chain, get_features, add_filters

# Global Variables
AVAILABLE_SYMBOLS = ["NIFTY", "BANKNIFTY", "FINNIFTY", "NIFTYNXT50", "MIDCNIFTY"]
AVAILABLE_EXPIRY = ["14 August", "21 August", "28 August"] # Implement the fetch function for valid expiry
# AVAILABLE_EXPIRY = get_expiry(...)
AVAILABLE_STRIKE_PRICE = [25000, 25500, 26000, 26500, 27000] # yet to implement
# VAILABLE_STRIKE_PRICE = get_strike_price(...)
TIME_DELAYS = ["1 Min", "3 Min", "5 Min"]


st.title("NSE Data Dashboard")

# Sidebar for Filters
with st.sidebar:
    st.header("Filters")
    
    symbol = st.selectbox("Symbol Name", AVAILABLE_SYMBOLS)
    expiry = st.selectbox("Expiry Date", AVAILABLE_EXPIRY)
    strike_price = st.multiselect("Strike Price", AVAILABLE_STRIKE_PRICE, default=AVAILABLE_STRIKE_PRICE[:1])
    time_delay = st.radio("Time Delay", TIME_DELAYS)
    
# Main Content
while True:
raw_data, expiry = fetch_option_chain(symbol=symbol)
processed_data = get_features(raw_data)
#filtered_data = add_filters(processed_data, expiry, strike_price, time_delay)
st.write(processed_data)
time.sleep(10)
st.write("bablu")

