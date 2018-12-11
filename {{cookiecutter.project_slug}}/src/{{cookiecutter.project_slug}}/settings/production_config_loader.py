import os

from seveno_pyutil import abspath_if_relative, is_blank

from .external_config_loader import ExternalConfigLoader


class ProductionConfigLoader(ExternalConfigLoader):
    """
    External config file loader for ``production`` mode of operation.

    In this mode of operation, application loads configuration in standard Linux way
    trying first at ``/etc``, then in ``$XDG_CONFIG_HOME``. Config files are loaded
    from multiple locations, and values loaded from ``$XDG_CONFIG_HOME`` replace
    values loaded from ``/etc``.

    **Config and log file locations**

    - application config file paths
        - value of ``--config-file-path`` if provided
        - else ``[/etc/{{cookiecutter.project_slug}}/app.yaml,
          $XDG_CONFIG_HOME/{{cookiecutter.project_slug}}/app.yaml]``

    - logging config JSON file path
        - value of ``--logging-config-path`` if provided
        - else ``[/etc/{{cookiecutter.project_slug}}/logging_config.json,
          $XDG_CONFIG_HOME/{{cookiecutter.project_slug}}/logging_config.json]``

    In case no logging config path can be loaded, application will use default
    bundled logging config.

    - application log file path
        - value of ``--log-file-path`` if provided
        - else value from logging_config.json if provided
        - else ``$XDG_DATA_HOME/{{cookiecutter.project_slug}}/log/production.log``

    **Resolving relative paths**

    If any of commandline arguments use relative paths, they are resolved into
    absolute ones:

        - if app is running from source repo, relative paths are resolved as relative
          to the repo root
        - if app is running from installed package, relative paths are resolved as
          relative to ``$XDG_CONFIG_HOME`` and ``$XDG_DATA_HOME``
    """

    DEBUG = False
    TESTING = False

    _FORCE_SINGLE_LINE_LOGS = True
    _FORCE_DISABLE_SYSLOG = False

    @property
    def filelog_abspath(self):
        cmdline = getattr(self.cmdline_args, "log_file_path", None)
        logging_json = (
            self.logging_json["handlers"].get("file", {}).get("filename", None)
        )

        retv = (
            (cmdline if not is_blank(cmdline) else None)
            or getattr(self, "FILELOG_PATH", None)
            or (logging_json if not is_blank(logging_json) else None)
            or os.path.join(self.XDG_DATA_HOME, "production.log")
        )

        return (
            abspath_if_relative(retv, relative_to=self._REPO_ROOT)
            if self._IS_RUNNING_FROM_SOURCE
            else abspath_if_relative(retv, relative_to=self.XDG_DATA_HOME)
        )

    @property
    def logging_config_abspaths(self):
        cmdline = getattr(self.cmdline_args, "logging_config_path", None)

        if not is_blank(cmdline):
            return [
                (
                    abspath_if_relative(cmdline, relative_to=self._REPO_ROOT)
                    if self._IS_RUNNING_FROM_SOURCE
                    else abspath_if_relative(cmdline, relative_to=self.XDG_CONFIG_HOME)
                )
            ]
        else:
            return [
                "/etc/{{cookiecutter.project_slug}}/logging_config.json",
                os.path.join(self.XDG_CONFIG_HOME, "logging_config.json"),
            ]

    @property
    def config_file_abspaths(self):
        cmdline = getattr(self.cmdline_args, "config_file_path", None)

        if not is_blank(cmdline):
            return [
                abspath_if_relative(cmdline, relative_to=self._REPO_ROOT)
                if self._IS_RUNNING_FROM_SOURCE
                else abspath_if_relative(cmdline, relative_to=self.XDG_CONFIG_HOME)
            ]
        else:
            return [
                "/etc/{{cookiecutter.project_slug}}/production.yaml",
                "/etc/{{cookiecutter.project_slug}}/production.yml",
                "/etc/{{cookiecutter.project_slug}}/app.yaml",
                "/etc/{{cookiecutter.project_slug}}/app.yml",
                os.path.join(self.XDG_CONFIG_HOME, "production.yaml"),
                os.path.join(self.XDG_CONFIG_HOME, "production.yml"),
                os.path.join(self.XDG_CONFIG_HOME, "app.yaml"),
                os.path.join(self.XDG_CONFIG_HOME, "app.yml"),
            ]
