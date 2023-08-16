FROM python:slim

RUN mkdir /app
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

COPY src/requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./
EXPOSE 80

CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "wsgi:server"]
