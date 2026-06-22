import plotly.express as px
import pandas as pd

def create_chart(df):

    if len(df.columns) < 2:
        return None

    x_col = df.columns[0]
    y_col = df.columns[1]

    # Check if second column is numeric
    if not pd.api.types.is_numeric_dtype(df[y_col]):
        return None

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title="Business Analysis"
    )

    return fig