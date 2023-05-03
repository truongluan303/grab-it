FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update -y
# Need ffmeg for youtube-dl
RUN apt-get install -y ffmpeg

COPY . .

# Flask will use port 5000
EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]
