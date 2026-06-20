from src.llm.text_to_sql import generate_sql
from src.analytics.query_executor import execute_query
from src.analytics.insights import generate_insights

question = "Show top 5 products by revenue"

sql = generate_sql(question)

print("Generated SQL:")
print(sql)

df = execute_query(sql)

print("\nResults:")
print(df)

insights = generate_insights(df)

print("\nInsights:")
print(insights)