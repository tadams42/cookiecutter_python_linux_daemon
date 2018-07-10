__version__ = "{{cookiecutter.version}}"

from .server import Server, create_app
from .settings import SETTINGS, ImproperlyConfiguredError
