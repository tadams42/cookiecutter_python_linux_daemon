# [Cookiecutter] Python linux daemon template

cookiecutter template for simple Python 3 Linux daemon application.

- setuptools deployable
- tests using [py.test]
- [Sphinx] docs
- [click] commandline interface
- 3 modes of application operation (development, test, production)
- logging by default to local file and syslog, but easily configurable
- logs all events as single line in production mode (great for syslog)

## Docs

Check the pretty [slides](https://tadams42.github.io/cookiecutter_python_linux_daemon/)

## Use it

~~~sh
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip wheel cookiecutter
cookiecutter cookiecutter-python-linux-daemon
~~~

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[click]: http://click.pocoo.org/6/
[Sphinx]: http://www.sphinx-doc.org/en/master/
[py.test]: https://docs.pytest.org/en/latest/
