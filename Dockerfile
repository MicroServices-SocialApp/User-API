# 1. Base Image: Use a lightweight Python version
FROM python:3.13-slim

# 2. Environment Variables
# Prevents Python from writing .pyc files and ensures logs are visible immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Work Directory inside the container
WORKDIR /app

# 4. Install System Dependencies
# gcc is required to build asyncpg's Python extensions
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python Dependencies
# Copy requirements first to leverage Docker caching
COPY req/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 6. Copy the Application Code
COPY . .

# 7. Expose the internal port
EXPOSE 8000

# 8. Start the Application
CMD python db/wait_for_db.py && uvicorn main:app --host 0.0.0.0 --port 8000
