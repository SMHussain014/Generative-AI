# How to play with Docker
- For Windows:
- 64-bit version of Windows 10/11
- Hardware virtualization support must be enabled in your system’s BIOS
- WSL 2 - in services enable this

# How to install Docker Desktop
- https://docs.docker.com/get-docker/

# How to check Docker Version
- docker -v
- docker version

# How to test Docker 
- docker run hello-world

# Building Python Dockerfiles with Poetry
- Base Image: We'll use python:3.12-slim as the base image
- ARG and ENV: https://vsupalov.com/docker-arg-env-variable-guide/

# Development Dockerfile:
FROM python:3.12-slim
LABEL maintainer="name and email"
WORKDIR /code
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install poetry
COPY . /code/   
RUN poetry config virtualenvs.create false
RUN poetry install
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "my_todos.main:app", "--host", "0.0.0.0", "--reload"]

# Building the Image:
- docker build -f Dockerfile.dev -t my-dev-image .

# Check Images:
- docker images
- docker image ls 
- docker inspect my-dev-image

# Running the Container:
- docker run -d --name dev-cont1 -p 8000:8000 my-dev-image
- docker run -it --name dev-cont1 -p 8000:8000 my-dev-image (run in interactive mode)

# Running the App in Browser
- http://localhost:8000

# List Running Containers
- docker ps
- docker ps -a
- docker container ls

# View Running Containers' logs
- docker logs container_name
- docker logs container_name -f (see live changes)

# Stop the Logs
- Press ctrl+C

# Opening the command line in the container:
- docker exec -it dev-cont1 /bin/bash

# How to come out from container
- type 'exit' and press enter

# How to test a container:
- docker run -it --rm my-dev-image /bin/bash -c poetry run pytest

# Production Dockerfile (Multi-Stage Build):
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
# Stage 2: Production image
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/lib/python3.12/site-packages .
COPY . .
ENTRYPOINT ["python", "main.py"]

# Explanation:
Stage 1:
Inherits from python:3.12-slim.
Sets working directory to /app.
Copies pyproject.toml.
Disables automatic virtual environment creation by Poetry.
Installs dependencies excluding development packages using poetry install --no-dev.
Stage 2:
Inherits from the same base image.
Sets working directory to /app.
Copies only the installed dependencies from the builder stage using COPY --from=builder /app/lib/python3.12/site-packages .. This significantly reduces the image size.
Copies the rest of the project files.
Sets the entry point to directly execute python main.py.

# Building the Image:
docker build -f Dockerfile.prod -t my-prod-image --target prod .
# Running the Container:
docker run -it my-prod-image