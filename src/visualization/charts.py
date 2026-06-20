import plotly.express as px

def create_chart(df):

    if len(df.columns) < 2:
        return None

    x_col = df.columns[0]
    y_col = df.columns[1]

    if len(df) <= 5:
        fig = px.pie(
            df,
            names=x_col,
            values=y_col,
            title="Distribution Analysis"
        )
    else:
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            title="Business Analysis"
        )

    return fig