import plotly.express as px
import pandas as pd

def create_chart(df, question):

    if len(df.columns) < 2:
        return None

    x_col = df.columns[0]
    y_col = df.columns[1]

    if not pd.api.types.is_numeric_dtype(df[y_col]):
        return None

    question = question.lower()

    # Pie Chart
    if any(word in question for word in [
        "distribution",
        "share",
        "percentage",
        "proportion",
        "contribution"
    ]):
        return px.pie(
            df,
            names=x_col,
            values=y_col,
            title="Distribution Analysis"
        )

    # Line Chart
    elif any(word in question for word in [
        "trend",
        "over time",
        "daily",
        "monthly",
        "yearly",
        "date"
    ]):
        return px.line(
            df,
            x=x_col,
            y=y_col,
            markers=True,
            title="Trend Analysis"
        )

    # Default Bar Chart
    else:
        return px.bar(
            df,
            x=x_col,
            y=y_col,
            title="Business Analysis"
        )