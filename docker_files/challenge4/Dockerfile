FROM python:3.10

WORKDIR /challenge4


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN pip install docker


EXPOSE 5000


CMD ["python", "app.py"]
