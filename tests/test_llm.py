from src.llm.text_to_sql import generate_sql

question = "Show top 5 products by revenue"

sql = generate_sql(question)

print(sql)