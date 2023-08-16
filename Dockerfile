FROM python:3.12-slim-bullseye

RUN mkdir /build
WORKDIR /build
COPY src/requirements.txt .
RUN pip3 install -r requirements.txt

COPY src/ ./
EXPOSE 80
CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "wsgi:server"]
