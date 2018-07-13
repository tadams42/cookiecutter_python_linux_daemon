# {{cookiecutter.project_slug}}

{{cookiecutter.project_slug}} service.

## Install

For development machine run:

~~~sh
sudo apt install python3-dev python3-venv libcap-de

python3 -mvenv .venv
source .venv/bin/activate
pip install  --editable .[dev]
~~~

For the rest of glory details see [INSTALL.md](INSTALL.md)

## Run

Running app shell and server:

~~~sh
source .venv/bin/activate
{{cookiecutter.project_slug}} runserver
{{cookiecutter.project_slug}} shell
{{cookiecutter.project_slug}} --help
~~~

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
py.test -p no:sugar --spec
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
git commit "Added dependency Foo..."
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
    bumpversion --dry-run patch
    bumpversion patch --commit
    ~~~
