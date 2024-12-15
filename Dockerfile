FROM python:3.10-slim
WORKDIR /app
COPY src/ /app/
RUN pip install --no-cache-dir flask pymongo
CMD ["python", "-u", "main.py"]
