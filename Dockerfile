# Base image with common settings
FROM python:3.11-slim AS python-base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Python logs appear in real time.
ENV PYTHONUNBUFFERED=1

# Add poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app


# Production image
FROM python-base AS production

# Install system dependencies, Poetry, and cleanup in one layer
RUN apt-get update && \
    apt-get install -y curl build-essential libpq-dev && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.create false

# Copy files
COPY . .

# Install production dependencies only and cleanup
RUN poetry install --no-root --without dev && \
    # Remove build dependencies and clean up
    apt-get purge -y build-essential curl && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Expose the production port
EXPOSE ${PORT:-8000}

# Run the production server
CMD poetry run gunicorn -w 5 -b 0.0.0.0:${PORT:-8000} page_analyzer:app


# Development image
FROM python-base AS development

# Install system dependencies and Poetry
RUN apt-get update && \
    apt-get install -y curl build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/* && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.create false

# Copy files
COPY . .

# Install dependencies including dev dependencies
RUN poetry install --no-root

# Expose the development port
EXPOSE ${PORT:-5050}

# Run the development server
CMD poetry run flask --app page_analyzer:app --debug run --host=0.0.0.0 --port=${PORT:-5050}
