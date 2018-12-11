import os

from pkg_resources import Requirement, resource_filename
from seveno_pyutil import is_blank

from .external_config_loader import ExternalConfigLoader, ImproperlyConfiguredError


class DevelopmentConfigLoader(ExternalConfigLoader):
    """
    External config file loader for ``development`` mode of operation.

    In this mode:

    - config is never loaded from system wide locations (to prevent automatic loading
      of production config when starting application in development mode)
    - command line arguments for ``--config-file-path``, ``--log-file-path`` and
      ``--logging-config-path`` don't allow relative paths and will rise exception in
      this mode of operation. Resolving relative path from within installed package
      is only possible by considering it relative to systemwide locations. since
      automatic use of systemwide config files in development mode is dangerous this
      is prevented but stated exception.

    **Config and log file locations**

    - application config file path
        - value of ``--config-file-path`` if provided and is absolute path
        - ``config/development.yaml`` if running from inside repo
        - bundled Python resource if running from installed package

    - logging config JSON file path
        - value of ``--logging-config-path`` if provided and is absolute path
        - ``config/logging_config.json`` if running from inside repo
        - bundled Python resource if running from installed package

    - application log file path
        - value of ``--log-file-path`` if provided and is absolute path
        - ``log/development.log`` if running from inside repo
        - ``/tmp/{{cookiecutter.project_slug}}.tmp/development.log`` if running from installed
          package
    """

    DEBUG = True
    TESTING = False

    _FORCE_SINGLE_LINE_LOGS = False
    _FORCE_DISABLE_SYSLOG = True

    @property
    def filelog_abspath(self):
        self._load_logging_config()

        non_default = getattr(
            self.cmdline_args, "log_file_path", None
        ) or self.logging_json["handlers"].get("file", {}).get("filename", None)

        if not is_blank(non_default):
            if not os.path.isabs(non_default):
                raise ImproperlyConfiguredError(
                    "Relative paths for --log-file-path are not allowed in "
                    "development mode!"
                )
            return non_default

        if self._IS_RUNNING_FROM_SOURCE:
            return os.path.join(self._REPO_ROOT, "log", "development.log")
        else:
            return os.path.join(self.DEFAULT_TEMP_DIR, "development.log")

    @property
    def logging_config_abspaths(self):
        cmdline = getattr(self.cmdline_args, "logging_config_path", None)

        if not is_blank(cmdline):
            if not os.path.isabs(cmdline):
                raise ImproperlyConfiguredError(
                    "Relative paths for --logging-config-path are not allowed "
                    "in development mode!"
                )
            return [cmdline]

        if self._IS_RUNNING_FROM_SOURCE:
            return [os.path.join(self._REPO_ROOT, "config", "logging_config.json")]
        else:
            return [
                resource_filename(
                    Requirement.parse("{{cookiecutter.project_slug}}"),
                    "{{cookiecutter.project_slug}}/resources/logging_config.json",
                )
            ]

    @property
    def config_file_abspaths(self):
        cmdline = getattr(self.cmdline_args, "config_file_path", None)

        if not is_blank(cmdline):
            if not os.path.isabs(cmdline):
                raise ImproperlyConfiguredError(
                    "Relative paths for --config-file-path are not allowed "
                    "in development mode!"
                )
            return [cmdline]

        if self._IS_RUNNING_FROM_SOURCE:
            return [os.path.join(self._REPO_ROOT, "config", "development.yaml")]
        else:
            return [
                resource_filename(
                    Requirement.parse("{{cookiecutter.project_slug}}"),
                    "{{cookiecutter.project_slug}}/resources/development.yaml",
                )
            ]
