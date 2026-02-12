# Docker Configuration for Backend

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (Skipping to save RAM on Railway Trial)
# If you need specific C-extensions, uncomment below, but it may hit RAM limits.
# RUN apt-get update && apt-get install -y gcc postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
