import pandas as pd
from src.database.db_connection import engine

def execute_query(sql):
    return pd.read_sql(sql, engine)