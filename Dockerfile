FROM python

WORKDIR /code

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# install docker
RUN apt update && apt install -y docker
RUN groupadd docker && usermod -aG docker root && newgrp docker

# copy source into container
COPY . .

# entrypoint
CMD [ "gunicorn", "-b", "0.0.0.0:9101", "--worker-tmp-dir", "/dev/shm", "--workers", "2", \
"--threads", "4", "--worker-class", "gthread", "--log-file", "-", "app:app" ]