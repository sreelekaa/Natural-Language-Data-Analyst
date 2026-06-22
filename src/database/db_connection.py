from sqlalchemy import create_engine
import streamlit as st
from urllib.parse import quote_plus

# Read values from Streamlit Secrets
DB_HOST = st.secrets["DB_HOST"]
DB_PORT = st.secrets["DB_PORT"]
DB_NAME = st.secrets["DB_NAME"]
DB_USER = st.secrets["DB_USER"]
DB_PASSWORD = st.secrets["DB_PASSWORD"]

# Encode password safely
password = quote_plus(DB_PASSWORD)

# Create connection
engine = create_engine(
    f"postgresql://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Test connection
try:
    conn = engine.connect()
    print("Database Connected Successfully!")
    conn.close()

except Exception as e:
    print("DATABASE ERROR:")
    print(str(e))
    raise