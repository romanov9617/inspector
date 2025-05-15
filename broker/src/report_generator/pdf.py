from reportlab.pdfgen import canvas
from pathlib import Path


def create_pdf(report):
    path = Path("/tmp") / f"report_{report.id}.pdf"
    c = canvas.Canvas(str(path))
    c.setFont("Helvetica", 14)
    c.drawString(50, 800, f"Report #{report.id}")
    y = 770
    for i, d in enumerate(report.defect_set.all(), 1):
        c.drawString(60, y, f"{i}) cls={d.class_code} conf={d.confidence:.2f}")
        y -= 18
    c.save()
    return str(path)
