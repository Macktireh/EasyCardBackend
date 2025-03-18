ARG PYTHON_BASE=3.12-slim

#############################################################################################
# -------------------------------------- build stage -------------------------------------- #
#############################################################################################
FROM python:$PYTHON_BASE AS builder

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y && \
  apt-get install -y --no-install-recommends gcc curl

RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false

ENV PADDLEOCR_MODEL_DIR=/project/.paddleocr
RUN mkdir -p ${PADDLEOCR_MODEL_DIR}/det/en \
    && mkdir -p ${PADDLEOCR_MODEL_DIR}/rec/en \
    && mkdir -p ${PADDLEOCR_MODEL_DIR}/cls \
    && curl -o ${PADDLEOCR_MODEL_DIR}/det/en/en_PP-OCRv3_det_infer.tar https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_det_infer.tar \
    && tar -xf ${PADDLEOCR_MODEL_DIR}/det/en/en_PP-OCRv3_det_infer.tar -C ${PADDLEOCR_MODEL_DIR}/det/en \
    && rm ${PADDLEOCR_MODEL_DIR}/det/en/en_PP-OCRv3_det_infer.tar \
    && curl -o ${PADDLEOCR_MODEL_DIR}/rec/en/en_PP-OCRv4_rec_infer.tar https://paddleocr.bj.bcebos.com/PP-OCRv4/english/en_PP-OCRv4_rec_infer.tar \
    && tar -xf ${PADDLEOCR_MODEL_DIR}/rec/en/en_PP-OCRv4_rec_infer.tar -C ${PADDLEOCR_MODEL_DIR}/rec/en \
    && rm ${PADDLEOCR_MODEL_DIR}/rec/en/en_PP-OCRv4_rec_infer.tar \
    && curl -o ${PADDLEOCR_MODEL_DIR}/cls/ch_ppocr_mobile_v2.0_cls_infer.tar https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar \
    && tar -xf ${PADDLEOCR_MODEL_DIR}/cls/ch_ppocr_mobile_v2.0_cls_infer.tar -C ${PADDLEOCR_MODEL_DIR}/cls \
    && rm ${PADDLEOCR_MODEL_DIR}/cls/ch_ppocr_mobile_v2.0_cls_infer.tar

COPY pyproject.toml pyproject.toml
COPY pdm.lock pdm.lock
RUN pdm install


#############################################################################################
# -------------------------------------- final stage -------------------------------------- #
#############################################################################################
FROM python:$PYTHON_BASE AS final

WORKDIR /project

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libgomp1 && rm -rf /var/lib/apt/lists/*

COPY --from=builder project/.venv /.venv
COPY --from=builder project/.paddleocr .paddleocr/
ENV PATH=/.venv/bin:$PATH
ENV PYTHONPATH=/project

COPY ./docker/local/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./docker/local/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY . .

RUN addgroup --system app && adduser --system --group app
USER app

ENTRYPOINT ["/entrypoint"]
