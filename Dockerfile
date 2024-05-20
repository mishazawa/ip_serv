FROM python:3.10-alpine

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt

COPY ./src /app/src

EXPOSE 80

CMD ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]

# FOR DEVELOPMENT PURPOSES
# CMD ["uvicorn", "src.main:app", "--reload", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
