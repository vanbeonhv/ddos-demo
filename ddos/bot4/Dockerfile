FROM python:3.10

RUN apt-get update && apt-get install -y \
    curl \
    && pip install scapy httpx\
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY bot.py /bot.py

CMD ["python", "-u", "/bot.py"]
