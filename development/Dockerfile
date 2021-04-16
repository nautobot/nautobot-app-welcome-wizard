FROM nniehoff/nautobot:v0.0.9

USER root

WORKDIR $NAUTOBOT_ROOT

# Upgrade pip and install poetry as well as configure poetry
RUN pip install --upgrade pip\
    && pip install poetry \
    && poetry config virtualenvs.create false

# -------------------------------------------------------------------------------------
# Install Nautobot Plugin
# -------------------------------------------------------------------------------------
WORKDIR /source

# Copy in only pyproject.toml/poetry.lock to help with caching this layer if no updates to dependencies
COPY poetry.lock pyproject.toml /source/
# --no-root declares not to install the project package since we're wanting to take advantage of caching dependency installation
# and the project is copied in and installed after this step
RUN poetry install --no-interaction --no-ansi --no-root

# Copy in the rest of the source code and install local Nautobot plugin
COPY . /source
RUN poetry install --no-interaction --no-ansi

WORKDIR $NAUTOBOT_ROOT
