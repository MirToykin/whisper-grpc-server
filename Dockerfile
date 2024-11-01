FROM python:3.12-slim

WORKDIR /app

# Copy files to the container
COPY . /app

# Install system dependencies for Whisper
RUN apt-get update && apt-get install -y ffmpeg

RUN pip install -r requirements.txt

# Run the server
CMD ["python", "run.py"]