FROM python:3.9-alpine

WORKDIR /code

# tell the API it's inside a container
ENV HOMEY_API_RUNNING_IN_DOCKER Yes

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# install docker-cli to communicate with mounted socket
RUN apk add --no-cache docker-cli

# copy source into container
COPY . .

# entrypoint
CMD [ "gunicorn", "-b", "0.0.0.0:9101", "--worker-tmp-dir", "/dev/shm", \
"--workers", "4", "--threads", "50", "--log-file", "-", "app:app" ]