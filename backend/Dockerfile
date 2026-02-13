# Docker Configuration for Backend
# Cache Buster: 2026-02-13T00:35:00

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (Skipping to save RAM on Railway Trial)
# If you need specific C-extensions, uncomment below, but it may hit RAM limits.
# RUN apt-get update && apt-get install -y gcc postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy everything at once
COPY . .

# Install dependencies
RUN python -m pip install --no-cache-dir -r requirements.txt

# Expose port (Railway will override this)
EXPOSE 8000

# Run application
# We run main.py directly; Pydantic Settings will automatically
# pick up the dynamic PORT variable from the environment.
CMD ["python", "main.py"]
