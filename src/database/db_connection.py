from sqlalchemy import create_engine
import streamlit as st

engine = create_engine(
    st.secrets["DATABASE_URL"]
)

try:
    conn = engine.connect()
    print("Database Connected Successfully!")
    conn.close()

except Exception as e:
    print("DATABASE ERROR:")
    print(str(e))
    raise