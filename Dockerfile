FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip -i https://mirror-pypi.runflare.com/simple && \
    pip install -r requirements.txt -i https://mirror-pypi.runflare.com/simple && \
    pip install debugpy -i https://mirror-pypi.runflare.com/simple

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
