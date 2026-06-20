
def validate_sql(sql):

    blocked_keywords = [
        "DROP",
        "DELETE",
        "UPDATE",
        "ALTER",
        "TRUNCATE",
        "INSERT"
    ]

    sql_upper = sql.upper()

    for keyword in blocked_keywords:
        if keyword in sql_upper:
            raise ValueError(
                f"Unsafe SQL detected: {keyword}"
            )

    return True

