FROM python:3.11.0a1-alpine3.14

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["tail", "-f", "/dev/null"]




