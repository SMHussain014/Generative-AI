# Pre-requisites:
- Python installed
- pip or pipx installed
- Poetry installed

# Create/ initialize a Project
- `poetry new project_name --name app_name`
- Go to the folder of project_name
- `type cd project_name and press enter`

# Create/ initialize virtual environment for the project
- `poetry run python --version`

# create a file namely 'main.py' in the folder 'app_name'
- After that set project environment by using:
- `poetry shell` or `poetry env list`

# How to add a package in the project
- `poetry add fastapi "uvicorn[standard]"` for server
- `poetry add pytest` for tests
- `poetry install` for all dependencies

# How to run the tests in CLI mode
- `poetry run pytest -v`

# How to run the project at server
- `poetry run uvicorn app.main:myApp --host localhost --port 8000` and press enter