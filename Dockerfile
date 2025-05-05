FROM python:3.8-slim

WORKDIR /

COPY . /

RUN apt-get update && apt-get install -y libgl1
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "handler.py"]