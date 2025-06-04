# Use the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables
ENV LANG=C.UTF-8

# Use apt interactive without ask user 
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip python3-dev ffmpeg git && rm -rf /var/lib/apt/lists/*
# Set the working directory
WORKDIR /app

# Clone the repo directly into /app
RUN git clone https://github.com/hmidani-abdelilah/Media-Downloader-API /app

# Create virtual environment and activate
RUN python3 -m venv .venv && \
    . .venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Run the application
CMD [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
