import pandas as pd
from flask import Flask
from time import sleep
from flask_apscheduler import APScheduler
from datetime import datetime, time

from fetch_data import fetch_option_chain
from data_processor import get_features
from storage import insert_data_from_df, truncate_data

app = Flask(__name__)
scheduler = APScheduler()

SYMBOLS = ['NIFTY', 'BANKNIFTY', 'FINNIFTY']

class Config:
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config())

def log_time():
    """Get current time without seconds."""
    return datetime.now().strftime("%H:%M")

def is_market_open():
    """Check if current time is within market hours and day is a weekday."""
    now = datetime.now()
    start_time = time(9, 15)  # Market opens at 9:15 AM
    end_time = time(15, 30)   # Market closes at 3:30 PM
    return now.weekday() < 5 and start_time <= now.time() <= end_time

def is_market_opening():
    """Check if current time is the market open time."""
    now = datetime.now()
    start_time = time(9, 15)  # Market opens at 9:15 AM
    return now.weekday() < 5 and now.time() == start_time

def scheduled_job(symbol):
    """Fetch, process, and store data if market is open."""
    current_time = log_time()
    
    if is_market_opening():
        print(f"[{current_time}] Market opening. Truncating dataset for {symbol}.")
        truncate_data(symbol)  # Clear or reset the dataset at market open
    
    if is_market_open():
        # print(f"[{current_time}] Starting job for {symbol}")
        data, expiry = fetch_option_chain(symbol)
        if data is not None:
            data_processed = get_features(data)
            insert_data_from_df(data_processed, symbol)
            print(f"[{current_time}] Data for {symbol} fetched successfully")
        else:
            print(f"[{current_time}] Failed to fetch data for {symbol}, skipping processing.")
    else:
        print(f"[{current_time}] Market is closed. Skipping job for {symbol}.")

scheduler.add_job(
    id=f'{SYMBOLS[0]}_fetch_and_store',
    func=scheduled_job,
    args=(SYMBOLS[0],),
    trigger='interval',
    minutes=1
)
sleep(5)
scheduler.add_job(
    id=f'{SYMBOLS[1]}_fetch_and_store',
    func=scheduled_job,
    args=(SYMBOLS[1],),
    trigger='interval',
    minutes=1
)
sleep(10)
scheduler.add_job(
    id=f'{SYMBOLS[2]}_fetch_and_store',
    func=scheduled_job,
    args=(SYMBOLS[2],),
    trigger='interval',
    minutes=1
)

scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    try:
        app.run(debug=False)
    except (KeyboardInterrupt, SystemExit):
        print("KeyboardInterrupt or SystemExit detected. Shutting down...")
        scheduler.shutdown()
        print("Scheduler shut down successfully.")
