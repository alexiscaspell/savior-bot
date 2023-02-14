FROM python:3.8

# RUN apt-get update
# RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /usr/app/

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ADD src/ src/
COPY app.py app.py

COPY .env .env

CMD [ "python","app.py" ]