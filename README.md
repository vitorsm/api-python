# api-python
Python API template.

This project is a template with boilerplate to Python APIs using Flask, SQLAlchemy and Injector.


## Setup

This project uses python 3.11. If you don't have it, you can install pyenv to manage different python versions.

Before install python using pyenv, you need to ensure some requirements:
```
sudo apt install -y libffi-dev
sudo apt install -y libsqlite3-dev sqlite3
```

After that, install pyenv:
```commandline
curl https://pyenv.run | bash
```

Now install python 3.11 and select it as default:
```
pyenv install 3.11.14
pyenv global 3.11.14
```

Create the virtual environment and install the dependencies:
``` 
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Tests coverage

Install the library coverage:
```
pip install coverage
```

Execute the tests using coverage:
```
coverage run -m unittest discover -s tests
```

Check the report of coverage:
```
coverage report -m
```

If you prefer, generate the html page for more details:
```
coverage html
```

## Deploy
Use the script resources/scripts/generate-version.sh to publish the docker image in docker hub.