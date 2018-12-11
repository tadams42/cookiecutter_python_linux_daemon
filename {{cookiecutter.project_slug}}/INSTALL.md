# Install

## Prerequisites

1. System dependencies

    ~~~sh
    sudo apt install python3-dev python3-venv libcap-dev redis-tools
    ~~~

2. External services

    * Redis
    * ...

## Development machines

### Install

~~~sh
python3 -m venv .venv
source .venv/bin/activate
pip install --editable .[dev]
~~~

### Configuration and logs

Location of configuration files depends on app startup mode (environment).

For `development` and `test` mode, config files are:

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

For any sensible development, you'll also need a bunch of services running. Simplest way to make that happen is to use provided docker-compose config:

~~~sh
# Starts services we depend on (ie. database server, Redis, etc...)
docker-compose --project-name {{cookiecutter.project_slug}} up --detach
~~~

This will start:

* Redis on `localhost:6379`

Now we can start application:

~~~sh
# Starts app server or shell in development mode of operation
source .venv/bin/activate
{{cookiecutter.project_slug}} runserver
{{cookiecutter.project_slug}} shell

# Starts app server or shell in other mode of operation
{{cookiecutter.project_slug}} -e test runserver
{{cookiecutter.project_slug}} -e production shell

# Strongly advised to run this one too, it shows useful info
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
python3 -m venv .venv
.venv/bin/python setup.py develop
~~~

**`setuptools` managed deployments**

Since our app is `setuptools` enabled it is also possible to build `sdist` package from it and place it into some kind of `pip` index. After that, installing app is equal to installing any other `pip` package.

~~~sh
python3 -m venv .venv
.venv/bin/pip --find-index https://.... install --update {{cookiecutter.project_slug}}
~~~

Note that when installed like this, app no longer has access to `log/` and `config/` directories. Instead, app behaves like any decent Linux software by following `$XDG_DATA_HOME` and `$XDG_CONFIG_HOME` from [XDG Base Directory Specification]

### Configuration and logs

In production mode, app expects and loads config files in following locations:

* `/etc/{{cookiecutter.project_slug}}/app.yaml`
* `$XDG_CONFIG_HOME/{{cookiecutter.project_slug}}/app.yaml`
* `{setup.py dir}/config/production.yaml`

and logs to one of following locations:

* `{setup.py dir}/log/production.log` when app is started from within the repo
* `$XDG_DATA_HOME/{{cookiecutter.project_slug}}/log/production.log` otherwise

It is possible to override these with command line parameters, for details see:

~~~sh
.venv/bin/{{cookiecutter.project_slug}} --help
~~~

### Run

Running development app shell or development app server with production config can be useful when trying to diagnose production problems:

~~~sh
.venv/bin/{{cookiecutter.project_slug}} runserver --environment production
.venv/bin/{{cookiecutter.project_slug}} shell --environment production
~~~

The simplest way to demonize application is to use [supervisord] with following configuration:

~~~ini
[{{cookiecutter.project_slug}}]
user=some_user
directory=/home/some_user/{{cookiecutter.project_slug}}
command=.venv/bin/{{cookiecutter.project_slug}} runserver --environment production
~~~

[supervisord]: http://www.supervisord.org
[systemd]: https://github.com/systemd/systemd
[XDG Base Directory Specification]: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
[Redis]: https://redis.io
