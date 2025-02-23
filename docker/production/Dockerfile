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
RUN pdm install --prod --no-editable


#############################################################################################
# -------------------------------------- final stage -------------------------------------- #
#############################################################################################
FROM python:$PYTHON_BASE

WORKDIR /project

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libgomp1 && rm -rf /var/lib/apt/lists/*

COPY --from=builder project/.venv .venv/
ENV PATH=/project/.venv/bin:$PATH
ENV PYTHONPATH=/project


COPY admin/ admin/
COPY commands/ commands/
COPY config/ config/
COPY controllers/ controllers/
COPY middlewares/ middlewares/
COPY migrations/ migrations/
COPY models/ models/
COPY repositories/ repositories/
COPY schemas/ schemas/
COPY services/ services/
COPY urls/ urls/
COPY utils/ utils/
COPY validators/ validators/
COPY main.py main.py

EXPOSE 5000

CMD [ "gunicorn", "main:app", "--bind", "0.0.0.0:5000", "--log-level", "info" ]
