FROM python:3.12-slim as base

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
COPY ./requirements requirements/
RUN pip install -r requirements/all.txt

# copy entrypoint script to container and make executable
COPY ./docker/local/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# copy start script to container and make executable
COPY ./docker/local/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy project
COPY . .

# run entrypoint
ENTRYPOINT ["/entrypoint"]
