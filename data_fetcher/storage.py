import pandas as pd
from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Float, String, DateTime, text
from sqlalchemy.engine import reflection

# Initialize the database engine and metadata
engine = create_engine('sqlite:///data.db')
metadata = MetaData()

def table_exists(table_name: str) -> bool:
    inspector = reflection.Inspector.from_engine(engine)
    return table_name in inspector.get_table_names()

def create_table_from_df(df: pd.DataFrame, table_name: str) -> Table:
    if df.empty:
        print(f"No data available to create table {table_name}.")
        return None

    if table_exists(table_name):
        # print(f"Table {table_name} already exists.")
        return Table(table_name, metadata, autoload_with=engine)

    column_types = {
        'object': String,
        'int64': Integer,
        'float64': Float,
        'datetime64[ns]': DateTime
    }

    table_columns = []
    for col in df.columns:
        col_type = column_types.get(str(df[col].dtype), String)
        table_columns.append(Column(col, col_type))

    if not table_columns:
        print(f"No valid columns found for table {table_name}.")
        return None

    table = Table(table_name, metadata, *table_columns, extend_existing=True)
    
    metadata.create_all(engine)
    
    return table


def insert_data_from_df(df: pd.DataFrame, table_name: str):
    """Insert data from a DataFrame into the specified table."""
    if df.empty:
        print(f"No data to insert into table {table_name}.")
        return

    table = create_table_from_df(df, table_name)
    if table is None:
        print(f"Table creation failed for {table_name}.")
        return

    df.to_sql(table.name, engine, if_exists='append', index=False)

def truncate_data(symbol: str):
    if not table_exists(table_name):
        print(f"Table {table_name} does not exist. No data to truncate.")
        return

    with engine.connect() as connection:
        query = text(f"DELETE FROM {table_name}")  # Delete all rows from the table
        connection.execute(query)
        print(f"Data for {symbol} has been truncated from the database.")
