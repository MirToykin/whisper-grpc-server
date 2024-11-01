FROM python:3.12-slim

WORKDIR /app

# Copy files to the container
COPY . /app

RUN mkdir -p /app/files

# Install system dependencies for Whisper
RUN apt-get update && apt-get install -y ffmpeg

RUN pip install -r requirements.txt

# Preload the Whisper model during the build
RUN python -c "import whisper; whisper.load_model('tiny')"

# Run the server
CMD ["python", "run.py"]