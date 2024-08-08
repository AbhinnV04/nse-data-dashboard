import streamlit as st
import pandas as pd
import time
from datetime import datetime
from nse_scraper import fetch_option_chain, get_features, add_filters, fetch_expiry_and_strikePrice

AVAILABLE_SYMBOLS = ["NIFTY", "BANKNIFTY", "FINNIFTY", "NIFTYNXT50", "MIDCNIFTY"]
AVAILABLE_STRIKE_PRICE, AVAILABLE_EXPIRY = fetch_expiry_and_strikePrice(symbol=AVAILABLE_SYMBOLS[0])  
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

raw_data, expiry_list = fetch_option_chain(symbol=symbol)
processed_data = get_features(raw_data)
processed_data = processed_data[processed_data["expiryDate"] == expiry]

now = datetime.now()
processed_data["Time"] = [now.strftime('%H:%M')] * processed_data.shape[0]     
processed_data["Date"] = [now.strftime('%Y-%m-%d')] * processed_data.shape[0]  
#filtered_data = add_filters(processed_data, expiry, strike_price, time_delay)
st.write(processed_data[processed_data["STRIKE_PRICE"].isin(strike_price)].reset_index(drop=True))


