FROM python:3.10.0-slim
ARG BOT_NAME=${BOT_NAME}

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"
RUN apt update && \
    apt install -y --no-install-recommends curl build-essential python3.10-venv python3-distutils && \
    python3 -m pip config set global.trusted-host "pypi.org files.pythonhosted.org" && \
    python3 -m pip install ensurepip
    useradd -M bot_user

# Adding manually because SSL doesn't work properly through AZ proxy
COPY install.python-poetry.org.txt ./
COPY poetry.lock pyproject.toml ./
RUN python3 install.python-poetry.org.txt -y && \
    /root/.local/share/pypoetry/bin/poetry install && \
    rm install.python-poetry.org.txt

USER bot_user
COPY . /usr/src/app/"${BOT_NAME:-tg_bot}"
