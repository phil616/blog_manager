
FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 1588

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "1588", "--lifespan", "on", "--log-config", "uvclogcfg.yml"]