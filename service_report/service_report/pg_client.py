import os
import psycopg
import json

PG_CONN = os.environ["PG_CONN"]


def get_pg_connection():
    return psycopg.connect(PG_CONN)


def save_report(conn, payload):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO reports (id, params, status) "
            "VALUES (%s, %s, 'READY')",
            (payload["report_id"], json.dumps(payload))
        )
    conn.commit()


def save_defects(conn, payload):
    with conn.cursor() as cur:
        for defect in payload.get("defects", []):
            cur.execute(
                "INSERT INTO "
                "defects (report_id, image_id, class_code, bbox, confidence) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    payload["report_id"],
                    payload.get("image_id"),
                    defect["class_code"],
                    json.dumps(defect["bbox"]),
                    defect.get("score", 0),
                )
            )
    conn.commit()


def get_report_by_id(conn, report_id):
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
        cur.execute(
            "SELECT id, params FROM reports WHERE id = %s", (report_id,))
        return cur.fetchone()


def mark_report_as_completed(conn, report_id, s3_key):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE reports SET status = 'COMPLETED', "
            "pdf_key = %s WHERE id = %s",
            (s3_key, report_id)
        )
    conn.commit()
