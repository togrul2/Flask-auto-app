FROM python:3.10-alpine
LABEL maintainer="Toghrul"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./apk_deps.sh /tmp/apk_deps.sh
COPY . /app

WORKDIR /app
EXPOSE 5000

RUN /tmp/apk_deps.sh && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser  \
    --disabled-password  \
    --no-create-home  \
    flask-user

ENV PATH="/py/bin/:$PATH"
USER flask-user