# {{cookiecutter.project_slug}}

{{cookiecutter.project_slug}} service.

## Install

~~~sh
sudo apt install python3-dev python3-venv libcap-dev redis-tools
python3 -m venv .venv
source .venv/bin/activate
pip install  --editable .[dev]
~~~

For the rest of glory details see [INSTALL.md](INSTALL.md)

## Run

Running app shell and server:

~~~sh
# Starts services we depend on (ie. database server, Redis, etc...)
docker-compose --project-name {{cookiecutter.project_slug}} up --detach

# Starts app server or shell in development mode of operation
source .venv/bin/activate
{{cookiecutter.project_slug}} runserver
{{cookiecutter.project_slug}} shell

# Strongly advised to run this one too, it shows useful info
{{cookiecutter.project_slug}} --help
~~~

For the rest of glory details see [INSTALL.md](INSTALL.md)

## Documentation

To generate and view very pretty docs:

~~~sh
source .venv/bin/activate
python setup.py build_sphinx
google-chrome build/sphinx/html/index.html
~~~

## Tests

To run tests:

~~~sh
py.test
~~~

Or with spec output:

~~~sh
py.test --spec
~~~

Or against multiple Python versions:

~~~sh
pip install tox
tox
~~~

## Maintaining dependencies

Add abstract dependencies to `requirements.in` and then:

~~~sh
pip install -U pip-tools
pip-compile requirements.in
git add requirements.*
git commit "Added dependences: Foo, Bar, Baz..."
~~~

## Releasing the thing checklist

1. Make sure repo is in good state:

    ~~~sh
    pip install tox
    tox
    ~~~

2. Make sure `CHANGELOG` is up to date.

3. Update version strings and commit:

    ~~~sh
    # For dev builds:
    bumpversion build --allow-dirty

    # or for hotfixes:
    bumpversion patch --allow-dirty

    # or for releases:
    bumpversion minor --allow-dirty
    bumpversion major --allow-dirty
    ~~~
