FROM python:3.12-slim

WORKDIR /app

# Install libatomic1 to satisfy Vosk dependencies
RUN apt-get update && apt-get install -y \
    libatomic1 \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy files to the container
COPY . /app

RUN mkdir -p /app/files
RUN mkdir -p /app/vosk

RUN pip install -r requirements.txt

# Run the server
CMD ["python", "run.py"]