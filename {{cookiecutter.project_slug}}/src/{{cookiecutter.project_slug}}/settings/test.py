import os

from pkg_resources import Requirement, resource_filename
from seveno_pyutil import is_blank

from .external_config_loader import (ExternalConfigLoader,
                                     ImproperlyConfiguredError)


class Test(ExternalConfigLoader):
    """
    External config file loader for ``test`` mode of operation.

    In this mode, config is never loaded from system wide locations. This is to
    prevent automatic loading of production config when starting application in
    test mode.

    Command line arguments for ``--config-file-path``, ``--log-file-path``
    and ``--logging-config-path`` don't allow relative paths and will rise
    exception in this mode of operation. Resolving relative path from
    installed package is only possible by considering it relative to
    systemwide locations, and as stated before, automatic use of systemwide
    config files in test mode is dangerous and thus prevented.

    **Config and log file locations**

    - application config file path
        - value of ``--config-file-path`` if provided and is absolute path
        - ``config/test.yaml`` if running from inside repo
        - bundled Python resource if running from installed package

    - logging config JSON file path
        - value of ``--logging-config-path`` if provided and is absolute path
        - ``config/logging_config.json`` if running from inside repo
        - bundled Python resource if running from installed package

    - application log file path
        - value of ``--log-file-path`` if provided and is absolute path
        - ``log/test.log`` if running from inside repo
        - ``/tmp/{{cookiecutter.project_slug}}.tmp/test.log`` if running from
          installed package
    """

    DEBUG = True
    TESTING = True

    FORCE_SINGLE_LINE_LOGS = False
    ENABLE_SYSLOG = False

    @property
    def filelog_abspath(self):
        non_default = (
            getattr(self.cmdline_args, 'log_file_path', None)
            or self.logging_json['handlers'].get('file', {}).get(
                'filename', None
            )
        )

        if not is_blank(non_default):
            if not os.path.isabs(non_default):
                raise ImproperlyConfiguredError(
                    "Relative paths for --log-file-path are not allowed in "
                    "test mode!"
                )
            return non_default

        if self._IS_RUNNING_FROM_SOURCE:
            return os.path.join(self._REPO_ROOT, "log", 'test.log')
        else:
            return os.path.join(self.DEFAULT_TEMP_DIR, "test.log")

    @property
    def logging_config_abspaths(self):
        cmdline = getattr(self.cmdline_args, 'logging_config_path', None)

        if not is_blank(cmdline):
            if not os.path.isabs(cmdline):
                raise ImproperlyConfiguredError(
                    "Relative paths for --logging-config-path are not allowed "
                    "in test mode!"
                )
            return [cmdline]

        if self._IS_RUNNING_FROM_SOURCE:
            return [os.path.join(
                self._REPO_ROOT, "config", 'logging_config.json'
            )]
        else:
            return [resource_filename(
                Requirement("{{cookiecutter.project_slug}}"),
                "{{cookiecutter.project_slug}}/resources/logging_config.json"
            )]

    @property
    def config_file_abspaths(self):
        cmdline = getattr(self.cmdline_args, 'config_file_path', None)

        if not is_blank(cmdline):
            if not os.path.isabs(cmdline):
                raise ImproperlyConfiguredError(
                    "Relative paths for --config-file-path are not allowed "
                    "in test mode!"
                )
            return [cmdline]

        if self._IS_RUNNING_FROM_SOURCE:
            return [os.path.join(self._REPO_ROOT, "config", 'test.yaml')]
        else:
            return [
                resource_filename(
                    Requirement("{{cookiecutter.project_slug}}"),
                    "{{cookiecutter.project_slug}}/resources/test.yaml"
                )
            ]
