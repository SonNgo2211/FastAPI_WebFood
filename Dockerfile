
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /app
COPY . .

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8000"]
