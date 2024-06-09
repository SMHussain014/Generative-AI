# How to write a yaml/yml file
version: "3.9"
name: mine_api
services:
  api:
    build:
      context: ./todosApp
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"  # Expose container port 8000 to host port 8000 ('-' is used to create an array)
 
# Some Commands
- 'docker compose version'
- 'docker compose config'
- `docker compose up -d`
- `docker compose up -d --build`
- `docker compose down`
- `docker compose stop`
- 'docker compose stop'
- 'docker compose start'
- 'docker compose ps'
- 'docker compose ls'

# How to view file in browser
- Go to browser and type specified localhost and press enter