import pandas as pd
from src.database.db_connection import engine

def get_tables():

    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public'
    """

    return pd.read_sql(query, engine)

def get_columns(table_name):

    query = f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name='{table_name}'
    """

    return pd.read_sql(query, engine)