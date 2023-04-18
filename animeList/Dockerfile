FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update \
    && apt-get install -y build-essential curl \
    && apt-get update \
    && curl https://sh.rustup.rs -sSf | bash -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["gunicorn", "app:app"]