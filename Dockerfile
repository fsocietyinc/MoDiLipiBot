FROM python:3.13-slim

WORKDIR /app

# Install pip dependencies from the lock/requirements file.
COPY requirements.txt pyproject.toml /app/
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy source and assets into the container.
COPY src /app/src
COPY assets /app/assets

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "modilipi_bot.main"]
