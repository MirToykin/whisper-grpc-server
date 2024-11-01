FROM python:3.13-slim

WORKDIR /app

# Copy files to the container
COPY . /app

# Install system dependencies for Whisper
RUN apt-get update && apt-get install -y ffmpeg

RUN pip install -r requirements.txt

# Preload the Whisper model during the build
RUN python -c "import whisper; whisper.load_model('tiny')"

# Run the server
CMD ["python", "run.py"]