Parablog - simple blogging platform
========

Set-up instructions
---------------

- Change directory into your newly created project.
```
cd parablog
```


- Create a Python virtual environment.
```
python -m venv env
```

- Upgrade packaging tools.
```
env/bin/pip install --upgrade pip setuptools
```

- Install the project in editable mode with its testing requirements.
```
env/bin/pip install -e ".[testing]"
```

- Configure the database.
```
env/bin/initialize_parablog_db development.ini
```

- Run your project's tests.
```
env/bin/pytest
```


- Run your project.
```
env/bin/pserve development.ini
```