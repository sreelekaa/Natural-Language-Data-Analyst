
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_sql(question):

    prompt = f"""
    You are a Senior PostgreSQL Database Expert.

    Database: PostgreSQL

    Table: sales

    Columns:
    id
    product_name
    category
    quantity
    revenue
    sale_date

    Rules:
    - Generate ONLY PostgreSQL compatible SQL.
    - Return ONLY SQL.
    - Use LIMIT instead of TOP.
    - Do NOT use WITH TIES.
    - Do NOT use UPDATE, DELETE, DROP, ALTER, TRUNCATE.
    - Only generate SELECT statements.
    - Use aggregation functions when appropriate.
    - For ranking questions use ORDER BY and LIMIT.

    Question:
    {question}
    """

    response = model.generate_content(prompt)

    sql = response.text

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.replace("WITH TIES", "")
    sql = sql.strip()

    return sql

