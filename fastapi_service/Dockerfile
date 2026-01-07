FROM python:3.12-slim

WORKDIR /fastapi_service

RUN apt-get update && apt-get install -y gcc

COPY requirements.txt /fastapi_service/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /fastapi_service/

ENV PYTHONPATH=/fastapi_service

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
