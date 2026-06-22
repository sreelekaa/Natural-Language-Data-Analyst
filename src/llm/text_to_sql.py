
import google.generativeai as genai
from dotenv import load_dotenv
import os
from src.database.schema_reader import get_schema
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")



def generate_sql(question):

    schema_df = get_schema()

    schema_text = ""

    for _, row in schema_df.iterrows():
        schema_text += (
            f"Table: {row['table_name']}, "
            f"Column: {row['column_name']}\n"
        )

    prompt = f"""
    You are a Senior PostgreSQL Database Expert.

    Database: PostgreSQL

    Database Schema:
    {schema_text}

    Rules:
    - Generate ONLY PostgreSQL compatible SQL.
    - Return ONLY SQL.
    - Use LIMIT instead of TOP.
    - Do NOT use WITH TIES.
    - Do NOT use UPDATE, DELETE, DROP, ALTER, TRUNCATE.
    - Only generate SELECT statements.
    - Use aggregation functions when appropriate.
    - For ranking questions use ORDER BY and LIMIT.
    - If uploaded_data exists, use it when relevant.
- Generate PostgreSQL SQL only.

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



