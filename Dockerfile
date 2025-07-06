FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      fail2ban \
      docker.io    \
      procps	\
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ ./bot

CMD ["python", "-u", "-m", "bot.main"]
