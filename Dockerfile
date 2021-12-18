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
CMD [ "python", "./app.py" ]