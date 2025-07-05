FROM python:3.11-slim

WORKDIR /app

# Ensure the package is discoverable
ENV PYTHONPATH=/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ ./bot

# Execute bot as a module so Python can resolve package imports correctly
CMD ["python", "-u", "-m", "bot.main"]
