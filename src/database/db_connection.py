from sqlalchemy import create_engine
import streamlit as st
from urllib.parse import quote_plus

password = quote_plus(
    st.secrets["DB_PASSWORD"]
)

engine = create_engine(
    f"postgresql://{st.secrets['DB_USER']}:{password}@"
    f"{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/"
    f"{st.secrets['DB_NAME']}"
)

try:
    conn = engine.connect()
    print("Database Connected Successfully!")
    conn.close()

except Exception as e:
    print("DATABASE ERROR:")
    print(str(e))
    raise