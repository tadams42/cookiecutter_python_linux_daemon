"""
App settings module providing access to global config singleton object.
"""

from objproxies import CallbackProxy
from seveno_pyutil import silent_remove

from .development_config_loader import DevelopmentConfigLoader
from .external_config_loader import ExternalConfigLoader, ImproperlyConfiguredError
from .production_config_loader import ProductionConfigLoader
from .test_config_loader import TestConfigLoader

#: Available app runtime environment types.
ENVIRONMENTS = {
    'development': DevelopmentConfigLoader,
    'test': TestConfigLoader,
    'production': ProductionConfigLoader
}

# Global config object instance
_SETTINGS = None


def init_module(environment, cmdline_args=None):
    """
    Initializes settings module and underlying objects with
        - contents of external config files.

    Note:
        Should be called once on app start.
    """
    global _SETTINGS
    _SETTINGS = ENVIRONMENTS[environment](cmdline_args=cmdline_args)
    _SETTINGS.load_and_validate()


def cleanup_module():
    try:
        silent_remove(_SETTINGS.instance_tmp_dir_path)
    except Exception:
        # Whatever, this is usually only called on app shutdown, and logging
        # here is just spam
        pass


# We must use CallbackProxy so that ``from {{cookiecutter.project_slug}}.settings import
# SETTINGS`` still returns _SETTINGS object even when _SETTINGS were
# initialized after import had happened

#: Global app settings. Available after calling `.init_module`.
SETTINGS = CallbackProxy(lambda: _SETTINGS)
