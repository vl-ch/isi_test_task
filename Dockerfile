FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/
COPY db_dump.json /app/
COPY entrypoint.sh /app/

EXPOSE 8000

CMD ["/app/entrypoint.sh"]