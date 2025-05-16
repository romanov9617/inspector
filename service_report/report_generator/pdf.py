from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path
import tempfile
import json


def create_pdf(report_row: tuple) -> Path:
    """
    Генерация PDF по строке отчёта из БД.
    report_row: tuple, полученный из psycopg cursor.fetchone()
    return: путь к PDF
    """

    report_id = str(report_row[0])
    params = report_row[1]

    if isinstance(params, str):
        params = json.loads(params)

    tmp_dir = Path(tempfile.gettempdir())
    pdf_path = tmp_dir / f'{report_id}.pdf'

    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    c.setFont('Helvetica', 14)
    c.drawString(100, 800, f'Report ID: {report_id}')
    c.setFont('Helvetica', 12)
    c.drawString(100, 780, f'Image ID: {params.get('image_id', '—')}')
    c.drawString(100, 760, f'Defect count: {len(params.get('defects', []))}')

    y = 730
    for i, d in enumerate(params.get('defects', []), start=1):
        c.drawString(
            100,
            y,
            f'{i}. class_code: {d['class_code']}, conf: {d.get('score', 0)}'
        )
        y -= 20
        if y < 100:
            c.showPage()
            y = 800

    c.save()
    return pdf_path
