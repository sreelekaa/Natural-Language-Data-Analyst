import pandas as pd
from src.database.db_connection import engine

def get_schema():

    query = """
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema='public'
    """

    return pd.read_sql(query, engine)