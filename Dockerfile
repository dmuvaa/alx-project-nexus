FROM python:3.11-slim

# Disable bytecode generation and set unbuffered output for better logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files at build time (optional)
# RUN python manage.py collectstatic --noinput

# Default command: run the application using Gunicorn
CMD ["gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]