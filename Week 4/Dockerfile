FROM python:3.11-slim

COPY persistent_auditor.py /app/

WORKDIR /data
VOLUME /data

CMD ["python", "-u", "/app/persistent_auditor.py"]
