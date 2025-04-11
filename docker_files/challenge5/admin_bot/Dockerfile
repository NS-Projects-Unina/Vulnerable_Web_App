FROM selenium/standalone-chrome:latest

USER root
WORKDIR /app
COPY admin_bot.py .

RUN apt-get update && apt-get install -y python3 python3-pip && pip3 install selenium --break-system-packages


CMD ["python3", "admin_bot.py"]
