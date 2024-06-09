# Install the latest version of Python onto your machine
# Make sure to check out and tick the box 'Set to Path Directory'

# Install 'pipx' onto your machine
- Open your terminal
- Install pipx using pip
- `python -m pip install --user pipx`
# Ensure pipx's binary directory is in your PATH
- `python -m pipx ensurepath`
- Restart your terminal to apply the PATH update

# Install 'Poetry' onto your machine
- `pipx install poetry`
- Copy path to your environment variable.

# Check whether poetry is installed globally onto your machine or not
- `poetry --version`
- If version is shown, its o.k., otherwise set environment variables

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
- `poetry add pytest` and so on... 
- 'poetry add update package'
- 'poetry add packages@latest'

# How to run the project in CLI mode
- `poetry run python app/main.py` and press enter
or
- `poetry run python ./app/main.py` and press enter

# How to run the tests in CLI mode
- `poetry run pytest -v`