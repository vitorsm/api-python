
FROM python:3.11

COPY . .
WORKDIR ./
RUN pip install -r requirements.txt

CMD ["uwsgi", "--http", ":8080", "-w", "src.wsgi:app", "--buffer-size", "32768"]
