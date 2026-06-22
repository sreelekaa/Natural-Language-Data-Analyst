import streamlit as st
import sys
import os
import pandas as pd

# Add project root to path
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
from src.validation.sql_validator import validate_sql
from src.reports.pdf_reports import generate_pdf
from src.database.db_explorer import (
    get_tables,
    get_columns
)
# --------------------------------
# Sidebar - Query History
# --------------------------------

history = pd.read_sql(
    """
    SELECT question
    FROM query_history
    ORDER BY created_at DESC
    LIMIT 10
    """,
    engine
)

st.sidebar.title("📜 Query History")

for q in history["question"]:
    st.sidebar.write("• " + q)
# -----------------------------
# Database Explorer
# -----------------------------

st.sidebar.markdown("---")
st.sidebar.header("📂 Database Explorer")

tables = get_tables()

selected_table = st.sidebar.selectbox(
    "Select Table",
    tables["table_name"]
)

columns = get_columns(selected_table)

st.sidebar.write("Columns:")

for col in columns["column_name"]:
    st.sidebar.write(f"• {col}")

st.sidebar.markdown("---")
st.sidebar.header("💡 Suggested Questions")

suggestions = [
    "Show top products by revenue",
    "Show revenue by category",
    "Show sales trend",
    "Show all customers"
]

for q in suggestions:
    st.sidebar.write("•", q)

total_queries = pd.read_sql(
    "SELECT COUNT(*) as total FROM query_history",
    engine
)

st.sidebar.metric(
    "Queries Run",
    int(total_queries["total"][0])
)
preview = pd.read_sql(
    f"SELECT * FROM {selected_table} LIMIT 5",
    engine
)

st.sidebar.write("Preview")
st.sidebar.dataframe(preview)
# --------------------------------
# Main Application
# --------------------------------

st.title("🤖 Natural Language Data Analyst")
# -----------------------------
# CSV /Excel Upload
# -----------------------------

st.subheader("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv","xlsx"]
)


if uploaded_file is not None:

    # Read file
    if uploaded_file.name.endswith(".csv"):

        uploaded_df = pd.read_csv(
            uploaded_file
        )

    elif uploaded_file.name.endswith(".xlsx"):

        uploaded_df = pd.read_excel(
            uploaded_file
        )

    # Save to PostgreSQL
    uploaded_df.to_sql(
        "uploaded_data",
        engine,
        if_exists="replace",
        index=False
    )

    st.success(
        "Dataset uploaded successfully!"
    )

    st.write("Preview")

    st.dataframe(
        uploaded_df.head()
    )

question = st.text_input(
    "Ask a business question"
)

if st.button("Analyze"):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    try:

        with st.spinner("Analyzing data..."):

            # Generate SQL
            sql = generate_sql(question)

            # Validate SQL
            validate_sql(sql)

            # Save Query History
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

            # Show SQL
            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            # Execute Query
            df = execute_query(sql)

            # Results
            st.subheader("Results")
            st.dataframe(df)

            # -------------------------
            # KPI Metrics
            # -------------------------

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

            numeric_cols = df.select_dtypes(include="number")

            if not numeric_cols.empty:

                total = numeric_cols.iloc[:, 0].sum()

                col3.metric(
                    "Total Value",
                    f"{total:,.0f}"
                )

            else:

                col3.metric(
                    "Total Value",
                    "N/A"
                )

            # -------------------------
            # CSV Download
            # -------------------------

            st.download_button(
                label="📥 Download Results as CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="query_results.csv",
                mime="text/csv"
            )

            # -------------------------
            # Visualization
            # -------------------------

            fig = create_chart(df,question)

            if fig is not None:

                st.subheader("Visualization")

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info(
                    "No chart available for this type of data."
                )

            # -------------------------
            # Insights
            # -------------------------

            st.subheader("Insights")

            insights = generate_insights(df)

            pdf_file = generate_pdf(
    question,
    sql,
    insights
)
            st.write(insights)
            with open(pdf_file, "rb") as file:

             st.download_button(
                label="📄 Download PDF Report",
                data=file,
                file_name="analysis_report.pdf",
                     mime="application/pdf"
                )

            st.success(
                "Analysis Completed Successfully!"
            )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )

# --------------------------------
# Footer
# --------------------------------

st.markdown("---")

st.caption(
    "Built with Gemini AI, PostgreSQL, Pandas, Plotly and Streamlit"
)