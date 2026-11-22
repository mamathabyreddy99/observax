FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 8000
# One worker + threads, so Prometheus counters live in a single process.
CMD ["gunicorn", "-w", "1", "--threads", "8", "-b", "0.0.0.0:8000", "app:app"]
