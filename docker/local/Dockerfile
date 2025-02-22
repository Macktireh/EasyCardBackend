ARG PYTHON_BASE=3.12-slim

#############################################################################################
# -------------------------------------- build stage -------------------------------------- #
#############################################################################################
FROM python:$PYTHON_BASE AS builder

# set work directory
WORKDIR /project

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y && \
  apt-get install -y --no-install-recommends gcc

RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false

COPY pyproject.toml pyproject.toml
COPY pdm.lock pdm.lock

# install dependencies and project into the local packages directory
RUN pdm install


#############################################################################################
# -------------------------------------- final stage -------------------------------------- #
#############################################################################################
FROM python:$PYTHON_BASE

WORKDIR /project

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libgomp1 && rm -rf /var/lib/apt/lists/*

COPY --from=builder project/.venv /.venv
ENV PATH=/.venv/bin:$PATH
ENV PYTHONPATH=/project/src

# copy start script to container and make executable
COPY ./docker/local/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy entrypoint script to container and make executable
COPY ./docker/local/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# copy project
COPY . .

# run entrypoint
ENTRYPOINT ["/entrypoint"]
