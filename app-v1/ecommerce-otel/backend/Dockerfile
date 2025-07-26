FROM python:3.10-slim
 
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*
 
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x ./wait-for-it.sh ./scripts/init_db.sh
CMD ["./wait-for-it.sh", "postgres:5432", "--", "sh", "-c", "./scripts/init_db.sh && uvicorn main:app --host 0.0.0.0 --port 8000"]
