"""
inference.py

Listens to Kafka for raw image bytes, runs model inference,
draws boxes and masks, and sends annotated images back to Kafka.
"""