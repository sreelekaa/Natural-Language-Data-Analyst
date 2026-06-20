import streamlit as st
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from sqlalchemy import text
from src.database.db_connection import engine
from src.llm.text_to_sql import generate_sql
from src.analytics.query_executor import execute_query
from src.analytics.insights import generate_insights
from src.visualization.charts import create_chart
import pandas as pd
from src.validation.sql_validator import validate_sql



# Sidebar Query History
history = pd.read_sql(
    """
    SELECT question
    FROM query_history
    ORDER BY created_at DESC
    LIMIT 10
    """,
    engine
)

st.sidebar.title("Query History")

for q in history["question"]:
    st.sidebar.write("• " + q)

st.title("Natural Language Data Analyst")

question = st.text_input("Ask a business question")

if st.button("Analyze"):

    sql = generate_sql(question)
    validate_sql(sql)
    # Save query history
    with engine.connect() as conn:
        conn.execute(
            text("""
            INSERT INTO query_history
            (question, generated_sql)
            VALUES (:question, :sql)
            """),
            {
                "question": question,
                "sql": sql
            }
        )
        conn.commit()

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    df = execute_query(sql)

    st.subheader("Results")
    st.dataframe(df)

    st.subheader("Quick Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
    "Rows Returned",
    len(df)
    )

    col2.metric(
    "Columns",
    len(df.columns)
    )

if len(df.columns) > 1:
    try:
        total = df.iloc[:, 1].sum()
        col3.metric(
            "Total Value",
            f"{total:,.0f}"
        )
    except:
        col3.metric(
            "Total Value",
            "N/A"
        )
    # CSV Download Button
    csv = df.to_csv(index=False)

    st.download_button(
    label="📥 Download Results as CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="query_results.csv",
    mime="text/csv"
    )
    fig = create_chart(df)

    st.subheader("Visualization")
    st.plotly_chart(fig, use_container_width=True)

    insights = generate_insights(df)

    st.subheader("Insights")
    st.write(insights)