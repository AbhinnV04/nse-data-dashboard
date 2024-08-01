# nse_scraper/data_processor.py
import pandas as pd

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
    
    return round_features(df)  