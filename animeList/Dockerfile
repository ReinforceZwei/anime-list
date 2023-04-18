FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update \
    && apt-get install -y python3-bcrypt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["gunicorn", "app:app"]