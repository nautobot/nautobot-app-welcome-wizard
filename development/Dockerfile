
ARG PYTHON_VER
ARG NAUTOBOT_VER
FROM ghcr.io/nautobot/nautobot-dev:${NAUTOBOT_VER}-py${PYTHON_VER} as welcome_wizard-dev

WORKDIR /source

# Copy in only pyproject.toml/poetry.lock to help with caching this layer if no updates to dependencies
COPY poetry.lock pyproject.toml /source/
# --no-root declares not to install the project package since we're wanting to take advantage of caching dependency installation
# and the project is copied in and installed after this step
RUN poetry install --no-interaction --no-ansi --no-root

# Copy in the rest of the source code and install local Nautobot plugin
COPY . /source
RUN poetry install --no-interaction --no-ansi

COPY development/nautobot_config.py /opt/nautobot/nautobot_config.py

FROM python:${PYTHON_VER}-slim as docs

ENV PYTHONUNBUFFERED=1

# Install all OS package upgrades and dependencies
# hadolint ignore=DL3005,DL3008,DL3013
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get autoremove -y && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/* && \
    pip --no-cache-dir install --upgrade pip wheel

RUN useradd --system --shell /bin/bash --create-home --home-dir /opt/welcome_wizard docs
WORKDIR /opt/welcome_wizard

COPY docs /opt/welcome_wizard/docs
COPY mkdocs.yml /opt/welcome_wizard

RUN pip install -r /opt/welcome_wizard/docs/requirements.txt

USER docs

CMD mkdocs serve -v -a 0.0.0.0:8080
