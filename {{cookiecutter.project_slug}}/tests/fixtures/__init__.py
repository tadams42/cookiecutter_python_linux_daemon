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

    This fixture doesn't start server, but creating (at least one) instance
    for test session is necessary so that app config is loaded and app
    environment is initialized.
    """
    app = Server("test")

    app.before_startup()

    def fin():
        app.before_shutdown()

    request.addfinalizer(fin)

    return app
