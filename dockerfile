FROM python:3.8-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
CMD python ./astroplan_bot.py