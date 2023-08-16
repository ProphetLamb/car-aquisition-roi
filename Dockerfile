FROM python:slim

RUN mkdir /app
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

COPY src/requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./
EXPOSE 8000

CMD [ "gunicorn", "-w=4", "-t=1", "car_aquisition_roi:server"]
