"""
Report-broker: слушает Kafka, сохраняет отчёты в БД и формирует PDF.
"""

# ───── sys.path + регистрация правильного admin ─────
import importlib.util
import sys
from pathlib import Path

# Путь до /app/admin/admin/admin/__init__.py
INNER_ADMIN = Path(__file__).resolve().parent.parent / "admin" / "admin" / "admin"
OUTER_ADMIN = INNER_ADMIN.parent  # /app/admin/admin

# Добавляем пути в sys.path
sys.path.insert(0, str(OUTER_ADMIN))                   # для admin.*
sys.path.insert(0, str(OUTER_ADMIN / "admin_modules")) # чтобы Django нашёл apps

# Регистрируем пакет admin
spec = importlib.util.spec_from_file_location("admin", INNER_ADMIN / "__init__.py")
admin_pkg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(admin_pkg)
admin_pkg.__path__.append(str(OUTER_ADMIN))            # чтобы видел admin_modules
sys.modules["admin"] = admin_pkg

# ─────────────── стандартные импорты ────────────────
import os
import json
import logging
import boto3
import django
from kafka import KafkaConsumer, KafkaProducer
from django.db import transaction

from admin.admin_modules.reports.models import Report, ReportStatus
from admin.admin_modules.defects.models import Defect
from broker.report_generator.pdf import create_pdf

# ─────────────── Django init ───────────────
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.admin.settings")
django.setup()

# ─────────────── external services ───────────────
BOOTSTRAP   = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
S3_ENDPOINT = os.getenv("S3_ENDPOINT_URL",       "http://minio:9000")
S3_BUCKET   = os.getenv("S3_BUCKET",             "inspector-reports")

s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id     = os.getenv("AWS_ACCESS_KEY_ID",     "1"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", "secret"),
)

consumer = KafkaConsumer(
    "processing.completed", "reports.pdf",
    bootstrap_servers   = BOOTSTRAP,
    group_id            = "report-broker",
    value_deserializer  = lambda m: json.loads(m.decode()),
    auto_offset_reset   = "earliest",
)

producer = KafkaProducer(
    bootstrap_servers = BOOTSTRAP,
    value_serializer  = lambda m: json.dumps(m).encode(),
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
LOG = logging.getLogger("broker")

# ─────────────── helpers ───────────────
@transaction.atomic
def save_report(payload: dict) -> str:
    rpt = Report.objects.create(params=payload, status=ReportStatus.READY)
    for d in payload.get("defects", []):
        Defect.objects.create(
            report     = rpt,
            image_id   = payload.get("image_id"),
            class_code = d["class_code"],
            bbox       = d["bbox"],
            confidence = d.get("score", 0),
        )
    LOG.info("Report %s saved (%s defects)", rpt.id, len(payload.get("defects", [])))
    return str(rpt.id)


def gen_and_upload(rid: str) -> str:
    rpt      = Report.objects.get(id=rid)
    pdf_path = create_pdf(rpt)
    key      = f"{rid}.pdf"
    s3.upload_file(pdf_path, S3_BUCKET, key)
    rpt.pdf_key = key
    rpt.status  = ReportStatus.COMPLETED
    rpt.save(update_fields=["pdf_key", "status"])
    return key


def send(topic: str, msg: dict):
    producer.send(topic, msg)
    producer.flush()

# ─────────────── main loop ───────────────
if __name__ == "__main__":
    LOG.info("🎧  report-broker started")
    for msg in consumer:
        try:
            if msg.topic == "processing.completed":
                save_report(msg.value)

            elif msg.topic == "reports.pdf":
                k = gen_and_upload(msg.value["report_id"])
                send("reports.created", {
                    "report_id": msg.value["report_id"],
                    "format":    "pdf",
                    "s3_key":    k,
                })
                LOG.info("Report %s uploaded → %s", msg.value["report_id"], k)

        except Exception as exc:
            LOG.exception("error on %s: %s", msg.topic, exc)
            send("reports.error", {"topic": msg.topic, "error": str(exc)})
