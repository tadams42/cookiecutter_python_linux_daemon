import os

import pytest
from faker import Faker

from {{cookiecutter.project_slug}} import Server

fake = Faker()
_SELF_PATH = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope="session", autouse=True)
def app(request, scope="session"):
    """
    Instance of Server. It doesn't start it, but creating it necessary for all
    app contexts initializations (ie. config is loaded and available through
    SETTINGS after this fixture).
    """
    app = Server("test")

    def fin():
        app.before_shutdown()

    request.addfinalizer(fin)
    return app
