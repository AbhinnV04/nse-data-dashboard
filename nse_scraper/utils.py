# nse_scraper/utils.py
import csv 
import os
import pandas as pd

def print_hr() -> None:
    print("|".rjust(70, "-"))
    return None

def write_to_csv(data: pd.DataFrame, file_path: str, columns: list) -> None:
    file_exists = os.path.exists(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        if not file_exists:
            writer.writeheader()
        for _, row in data.iterrows():
            writer.writerow(row[columns].to_dict())
    return None

def initialize_csv_file(file, columns) -> None:
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
    return None