FROM python:3.12.2-bookworm

WORKDIR /app/

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["./docker-entrypoint.sh"]
