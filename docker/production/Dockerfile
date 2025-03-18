ARG PYTHON_BASE=3.12-slim

#############################################################################################
# -------------------------------------- build stage -------------------------------------- #
#############################################################################################
FROM python:$PYTHON_BASE AS builder

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PDM_CHECK_UPDATE=false \
  PADDLEOCR_MODEL_DIR_DET=/project/.paddleocr/det/en \
  PADDLEOCR_MODEL_DIR_REC=/project/.paddleocr/rec/en \
  PADDLEOCR_MODEL_DIR_CLS=/project/.paddleocr/cls

RUN apt-get update && apt-get install -y --no-install-recommends gcc curl && \
  apt-get clean && rm -rf /var/lib/apt/lists/* && \
  pip install --upgrade pip && \
  pip install -U pdm

RUN mkdir -p ${PADDLEOCR_MODEL_DIR_DET} \
  && mkdir -p ${PADDLEOCR_MODEL_DIR_REC} \
  && mkdir -p ${PADDLEOCR_MODEL_DIR_CLS} \
  && curl -o ${PADDLEOCR_MODEL_DIR_DET}/en_PP-OCRv3_det_infer.tar https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_det_infer.tar \
  && tar -xf ${PADDLEOCR_MODEL_DIR_DET}/en_PP-OCRv3_det_infer.tar -C ${PADDLEOCR_MODEL_DIR_DET} --strip-components=1 \
  && rm ${PADDLEOCR_MODEL_DIR_DET}/en_PP-OCRv3_det_infer.tar \
  && curl -o ${PADDLEOCR_MODEL_DIR_REC}/en_PP-OCRv4_rec_infer.tar https://paddleocr.bj.bcebos.com/PP-OCRv4/english/en_PP-OCRv4_rec_infer.tar \
  && tar -xf ${PADDLEOCR_MODEL_DIR_REC}/en_PP-OCRv4_rec_infer.tar -C ${PADDLEOCR_MODEL_DIR_REC} --strip-components=1 \
  && rm ${PADDLEOCR_MODEL_DIR_REC}/en_PP-OCRv4_rec_infer.tar \
  && curl -o ${PADDLEOCR_MODEL_DIR_CLS}/ch_ppocr_mobile_v2.0_cls_infer.tar https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar \
  && tar -xf ${PADDLEOCR_MODEL_DIR_CLS}/ch_ppocr_mobile_v2.0_cls_infer.tar -C ${PADDLEOCR_MODEL_DIR_CLS} --strip-components=1 \
  && rm ${PADDLEOCR_MODEL_DIR_CLS}/ch_ppocr_mobile_v2.0_cls_infer.tar

COPY pyproject.toml pdm.lock ./
RUN pdm install --prod --no-editable


#############################################################################################
# -------------------------------------- final stage -------------------------------------- #
#############################################################################################
FROM python:$PYTHON_BASE AS final

WORKDIR /project

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libgomp1 && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

RUN addgroup --system app && adduser --system --group app
USER app

COPY --from=builder project/.venv .venv/
COPY --from=builder project/.paddleocr .paddleocr/

ENV PATH="/project/.venv/bin:$PATH" \
  PYTHONPATH="/project"

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

EXPOSE 8000

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--log-level", "info"]
