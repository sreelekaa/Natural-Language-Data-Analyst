from src.llm.text_to_sql import model

def generate_insights(df):

    prompt = f"""
    Analyze this sales data and provide:

    1. Key Findings
    2. Trends
    3. Recommendations

    Data:

    {df.to_string()}
    """

    response = model.generate_content(prompt)

    return response.text