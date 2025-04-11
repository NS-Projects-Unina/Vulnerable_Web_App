FROM python:3.9-slim

WORKDIR /app
COPY app.py flag.txt ./


RUN apt-get update && \
    apt-get install -y iputils-ping && \
    pip install flask

EXPOSE 5000
CMD ["python", "app.py"]
