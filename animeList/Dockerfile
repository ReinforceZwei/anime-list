FROM python:3.11

ENV TZ=Asia/Hong_Kong

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["gunicorn", "app:app"]