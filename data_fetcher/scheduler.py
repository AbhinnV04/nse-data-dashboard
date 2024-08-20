import pandas as pd
from flask import Flask
from time import sleep
from flask_apscheduler import APScheduler
from datetime import datetime

from fetch_data import fetch_option_chain
from data_processor import get_features
from storage import insert_data_from_df

app = Flask(__name__)
scheduler = APScheduler()

SYMBOLS = ['NIFTY', 'BANKNIFTY', 'FINNIFTY']

class Config:
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config())

def log_time():
    """Get current time without seconds."""
    return datetime.now().strftime("%H:%M")

def scheduled_job(symbol):
    current_time = log_time()
    print(f"[{current_time}] Starting job for {symbol}")
    data, expiry = fetch_option_chain(symbol)
    if data is not None:
        data_processed = get_features(data)
        insert_data_from_df(data_processed, symbol)
        print(f"[{current_time}] Data for {symbol} fetched successfully")
    else:
        print(f"[{current_time}] Failed to fetch data for {symbol}, skipping processing.")

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

if __nam.e__ == '__main__':
    try:
        app.run(debug=False)
    except (KeyboardInterrupt, SystemExit):
        print("KeyboardInterrupt or SystemExit detected. Shutting down...")
        scheduler.shutdown()
        print("Scheduler shut down successfully.")
