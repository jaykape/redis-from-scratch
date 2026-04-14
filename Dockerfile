FROM python:3.11-slim

WORKDIR /redis-from-scratch

COPY pyproject.toml .
COPY app ./app

RUN pip install .

EXPOSE 6379

CMD ["python", "-m", "app.main"]