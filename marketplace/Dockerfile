# Base Python image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files (from marketplace/ into /app/)
COPY . /app/

# Collect static files (ignore errors if no static setup yet)
RUN python manage.py collectstatic --noinput || true

# Expose port 8000 for Render
EXPOSE 8000

# Run the app
CMD ["gunicorn", "marketplace.wsgi:application", "--bind", "0.0.0.0:8000"]
