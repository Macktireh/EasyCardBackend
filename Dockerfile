ARG PYTHON_BASE=3.12-slim

#############################################################################################
# -------------------------------------- build stage -------------------------------------- #
#############################################################################################
FROM python:$PYTHON_BASE AS builder

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PDM_CHECK_UPDATE=false

RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install -U pdm

COPY pyproject.toml pdm.lock ./

RUN pdm install --prod --no-editable


#############################################################################################
# -------------------------------------- final stage -------------------------------------- #
#############################################################################################
FROM python:$PYTHON_BASE

WORKDIR /project

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libgomp1 && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

RUN addgroup --system app && adduser --system --group app
USER app

COPY --from=builder project/.venv .venv/

ENV PATH="/project/.venv/bin:$PATH" \
  PYTHONPATH="/project"

RUN find .venv -name '*.pyc' -delete && find .venv -name '__pycache__' -delete

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

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000", "--workers=4", "--timeout=30", "--log-level=info"]
