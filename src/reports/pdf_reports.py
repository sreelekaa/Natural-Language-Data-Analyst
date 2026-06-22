from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(
    question,
    sql,
    insights,
    filename="report.pdf"
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Natural Language Data Analyst Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"<b>Question:</b> {question}",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"<b>Generated SQL:</b><br/>{sql}",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"<b>Insights:</b><br/>{insights}",
            styles["BodyText"]
        )
    )

    doc.build(content)

    return filename