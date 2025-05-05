FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

 COPY . /

 RUN pip install --upgrade pip
 RUN pip install -r requirements.txt

 CMD ["python", "handler.py"]