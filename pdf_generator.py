from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

def create_pdf(content, filename):

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading1"]
    )

    normal_style = styles["BodyText"]

    story = []

    lines = content.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            story.append(Spacer(1, 10))
            continue

        if (
            "RESUME SUMMARY" in line.upper()
            or "COVER LETTER" in line.upper()
            or "ATS ANALYSIS" in line.upper()
        ):
            story.append(
                Paragraph(line, heading_style)
            )
            story.append(
                Spacer(1, 12)
            )
        else:
            story.append(
                Paragraph(line, normal_style)
            )
            story.append(
                Spacer(1, 6)
            )

    pdf.build(story)

    return filename