# Install

## Prerequisites

1. System dependencies

    ~~~sh
    sudo apt install python3-dev python3-venv libcap-dev
    ~~~

2. External services dependencies

    * ...

## Development machines

### Install

~~~sh
python3 -mvenv .venv
source .venv/bin/activate
pip install --editable .[dev]
~~~

For any sensible development, you'll also need a bunch of services running. Simplest way to make that happen is to use Docker:

~~~
cd bin
docker-compose up -d
~~~

### Configuration and logs

Config files are:

~~~sh
config/development.yaml
config/test.yaml
config/logging_config.json
~~~

And logs are in:

~~~sh
log/development.log
log/test.log
~~~

### Run

~~~sh
{{cookiecutter.project_slug}} runserver
{{cookiecutter.project_slug}} shell
{{cookiecutter.project_slug}} --help
~~~

## Production servers

### Install

There are two choices for production. We either deploy using `git` or we deploy using `setuptools`. For completeness sake, we describe both installs, but:

* For applications, `git` managed deployments are preferred. Main benefit here is ability of running `git status` inside of production-deployed app directory.
* For packages, `setuptools` managed deployments are preferred. Main benefit here is ability to put package into `pip` repository and let apps install it naturally like all other Python dependencies.

For both, packages and applications, there is another important benefit of enabling `setuptools` - running tests on installed version of our code (see for example [`pytest` - Choosing a test layout](https://docs.pytest.org/en/latest/goodpractices.html#choosing-a-test-layout-import-rules) and [Packaging a Python library](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure)).

**`git` managed deployments**

In this scenario, we `git clone` the repo to production server and then install
application into virtual environment:

~~~sh
git clone https://.../{{cookiecutter.project_slug}}
cd {{cookiecutter.project_slug}}
python3 -mvenv .venv
.venv/bin/python setup.py develop
~~~

**`setuptools` managed deployments**

Since our app is `setuptools` enabled it is also possible to build `sdist` package from it and place it into some kind of `pip` index. After that, installing app is equal to installing any other `pip` package.

~~~sh
python3 -mvenv .venv
.venv/bin/pip --find-index https://.... install --update {{cookiecutter.project_slug}}
~~~

Note that when installed like this, app no longer has access to `log/` and `config/` directories. Instead, app behaves like any decent Linux software by following `$$XDG_DATA_HOME` and `$XDG_CONFIG_HOME` from [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)

### Configuration and logs

In production mode, app expects and loads config files in following locations:

* `/etc/{{cookiecutter.project_slug}}/app.yaml`
* `$HOME/.config/{{cookiecutter.project_slug}}/app.yaml`
* `{setup.py dir}/config/production.yaml`

and logs to one of following locations:

* `{setup.py dir}/log/production.log` when app is started from within the repo
* `~/.local/share/{{cookiecutter.project_slug}}/log/production.log` otherwise

It is possible to override these with command line parameters, for details see:

~~~sh
.venv/bin/{{cookiecutter.project_slug}} --help
~~~

### Run

~~~sh
.venv/bin/{{cookiecutter.project_slug}} runserver --environment production
.venv/bin/{{cookiecutter.project_slug}} shell --environment production
.venv/bin/{{cookiecutter.project_slug}} --help
~~~

The simplest way to demonize application is to use `supervisord` with following configuration:

~~~ini
[{{cookiecutter.project_slug}}]
user=some_user
directory=/home/some_user/{{cookiecutter.project_slug}}
command=.venv/bin/{{cookiecutter.project_slug}} runserver --environment production
~~~
