import logging
from report_generator.pdf import create_pdf
from service_report.s3_client import upload_pdf_to_s3
from service_report.service_report.pg_client import (
    get_pg_connection,
    save_report,
    save_defects,
    get_report_by_id,
    mark_report_as_completed,
)
from service_report.kafka_producer import send_kafka_message

LOG = logging.getLogger("report-service")


def handle_processing_completed(payload: dict) -> None:
    with get_pg_connection() as conn:
        save_report(conn, payload)
        save_defects(conn, payload)
        LOG.info("Report %s saved with %d defects",
                 payload["report_id"], len(payload.get("defects", [])))


def handle_reports_pdf(payload: dict) -> None:
    report_id = payload["report_id"]
    with get_pg_connection() as conn:
        report = get_report_by_id(conn, report_id)
        if not report:
            raise ValueError(f"Report {report_id} not found")

        pdf_path = create_pdf(report)
        key = f"{report_id}.pdf"
        upload_pdf_to_s3(pdf_path, key)
        mark_report_as_completed(conn, report_id, key)

        send_kafka_message("reports.created", {
            "report_id": report_id,
            "format": "pdf",
            "s3_key": key,
        })
