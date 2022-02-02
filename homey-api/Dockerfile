FROM python:3.9-alpine

WORKDIR /code

# tell the API it's inside a container
ENV HOMEY_API_RUNNING_IN_DOCKER Yes

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# install docker-cli to communicate with mounted socket
RUN apk update --no-cache && apk add --no-cache docker-cli openrc && apk clean

# copy source into container
COPY . .

# entrypoint
CMD [ "gunicorn", "-b", "0.0.0.0:9101", "--worker-tmp-dir", "/dev/shm", "--workers", "2", \
"--threads", "4", "--worker-class", "gthread", "--log-file", "-", "app:app" ]