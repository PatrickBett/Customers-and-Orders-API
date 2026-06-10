# # Base Python image
# FROM python:3.13-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set work directory
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# COPY marketplace/requirements.txt /app/

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# RUN pip install gunicorn
# # Copy project files
# COPY . /app/

# # Collect static files (if any)
# RUN python manage.py collectstatic --noinput || true

# # Add inner 'marketplace' folder to PYTHONPATH
# ENV PYTHONPATH=/app/marketplace

# # Expose port 8000 for Render
# EXPOSE 8000
# # Run the app
# # CMD ["gunicorn", "marketplace.wsgi:application", "--bind", "0.0.0.0:$PORT"]
# # CMD gunicorn marketplace.wsgi:application --bind 0.0.0.0:$PORT
# # CMD gunicorn marketplace.marketplace.wsgi:application --bind 0.0.0.0:$PORT
# # CMD ["gunicorn", "marketplace.marketplace.wsgi:application", "--bind", "0.0.0.0:$PORT"]
# # ENTRYPOINT ["sh", "-c", "gunicorn marketplace.wsgi:application --bind 0.0.0.0:$PORT"]
# ENTRYPOINT ["/app/entrypoint.sh"]
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# requirements
COPY marketplace/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN pip install gunicorn

# copy project
COPY . /app/

# IMPORTANT: run Django from the manage.py location
WORKDIR /app/marketplace

# entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["/app/entrypoint.sh"]