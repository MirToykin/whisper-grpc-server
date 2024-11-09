FROM python:3.12-slim

WORKDIR /app

# Copy files to the container
COPY . /app

RUN mkdir -p /app/files
RUN mkdir -p /app/vosk

RUN pip install -r requirements.txt

# Run the server
CMD ["python", "run.py"]