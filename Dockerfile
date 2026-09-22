FROM python:3.11-slim

WORKDIR /app

# Install dependencies first so this layer caches when only code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app (code + models/)
COPY . .

EXPOSE 8501

# Fail the build early if the app file is missing
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
