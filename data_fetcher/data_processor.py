import pandas as pd
from datetime import datetime

def round_features(df) -> pd.DataFrame:
    df = df.round({
        "CE_OI": 0, "CE_CHNG_IN_OI": 0, "CE_VOLUME": 0, "CE_IV": 2, "CE_LTP": 2, "CE_CHNG": 2,
        "CE_BID_QTY": 0, "CE_BID_PRICE": 2, "CE_ASK_QTY": 0, "CE_ASK_PRICE": 2,
        "PE_OI": 0, "PE_CHNG_IN_OI": 0, "PE_VOLUME": 0, "PE_IV": 2, "PE_LTP": 2, "PE_CHNG": 2,
        "PE_BID_QTY": 0, "PE_BID_PRICE": 2, "PE_ASK_QTY": 0, "PE_ASK_PRICE": 2,
        "strikePrice": 2, "Spot Price": 2
    })
    return df

def calculate_deltas(df) -> pd.DataFrame:
    df["CE_Delta"] = df["CE_CHNG_IN_OI"].diff(-1)
    df["PE_Delta"] = df["PE_CHNG_IN_OI"].diff(-1)
    df["PCR"] = df["PE_OI"] / df["CE_OI"]
    return df


def get_ce_data(option_chain_data_df) -> pd.DataFrame:
    option_chain_ce = pd.DataFrame()
    option_chain_ce['CE'] = option_chain_data_df['CE']
    return pd.concat([option_chain_ce.drop('CE', axis=1), option_chain_ce['CE'].apply(pd.Series)], axis=1)

def get_pe_data(option_chain_data_df) -> pd.DataFrame:
    option_chain_pe = pd.DataFrame()
    option_chain_pe['PE'] = option_chain_data_df['PE']
    return pd.concat([option_chain_pe.drop('PE', axis=1), option_chain_pe['PE'].apply(pd.Series)], axis=1)

def get_features(src_data) -> pd.DataFrame:
    if src_data.empty:
        print("No data available for processing.")
        return pd.DataFrame()  
    
    ce_data = get_ce_data(src_data)
    pe_data = get_pe_data(src_data)
    
    df = pd.DataFrame()
    df["SPOT_PRICE"] = ce_data['underlyingValue']
    
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
    
    df["STRIKE_PRICE"] = src_data['strikePrice']
    
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
    df["expiryDate"] = pe_data["expiryDate"]
    df = round_features(df)
    df = calculate_deltas(df)
    
    df["DateTime"] = datetime.now().strftime("%H:%M")
    return df

