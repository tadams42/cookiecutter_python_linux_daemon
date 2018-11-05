import os

import pytest
from faker import Faker

from {{cookiecutter.project_slug}} import Server

fake = Faker()
_SELF_PATH = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope="session", autouse=True)
def app(request):
    """
    Instance of test `Server`.

    It doesn't ``startup`` server but it does ensure everything is initialized
    as though instance was actually started.
    """
    app = Server("test")

    app.before_startup()

    def fin():
        app.before_shutdown()

    request.addfinalizer(fin)

    return app
