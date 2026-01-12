FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project
COPY . .

EXPOSE 8000

# The command will be overridden by docker-compose to run db_setup first
CMD ["fastapi", "dev", "backend/main.py", "--host", "0.0.0.0", "--port", "8000"]
