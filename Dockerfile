FROM python:3.10.0-slim
ARG BOT_NAME=mud_bot
ARG POETRY_HOME=/usr/src/poetry


RUN apt update && \
    apt install -y --no-install-recommends curl build-essential libpq-dev && \
    apt clean && useradd bot_user

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"
COPY poetry.lock pyproject.toml ./

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN curl -sSl https://install.python-poetry.org | python3 - && \
    $POETRY_HOME/bin/poetry install --no-cache --with=dev

# Additional RUN slightly bloats the image, but prevents running the previous
# block every time I make a change to the code
COPY . /usr/src/app/"${BOT_NAME:-tg_bot}"
RUN  chown -R bot_user:bot_user /usr/src/

USER bot_user

ENTRYPOINT /usr/src/poetry/bin/poetry run python3 -m bot
CMD tail -f /dev/null >/dev/null