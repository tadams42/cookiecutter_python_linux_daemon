import json
import logging
import os
import tempfile
import uuid
from abc import ABC, abstractmethod
from collections import namedtuple
from logging.config import dictConfig
from typing import List, NamedTuple

import yaml
from pkg_resources import Requirement, resource_filename
from seveno_pyutil import (abspath_if_relative, current_user_home, is_blank,
                           silent_create_dirs)

_SELF_DIR = os.path.dirname(os.path.abspath(__file__))
_SETUP_PY_PATH = os.path.abspath(
    os.path.join(_SELF_DIR, '..', '..', '..', 'setup.py')
)


class ImproperlyConfiguredError(RuntimeError):

    pass


class ExternalConfigLoader(ABC):
    """
    External config file loader.

    External config is loaded from two types of files: main config file
    (.yaml) and logging config file (JSON).

    Loader is capable of loading same config file type from multiple locations
    simultaneously. This is usefull when you want to have system-wide config
    (ie. in ``/etc``) and also be able to override values of it per user (ie.
    in ``~/.config``).

    Subclasses implement concrete config environments which are a list of
    config files' locations that will be loaded. ``ExternalConfigLoader``
    implements actual loading of files in that list.

    Loader also receives and memoizes command line arguments that are used to
    override some or all config file locations and config values.

    Arguments:
        cmdline_args: Command line arguments.
    """

    #: Base name of application process. This name will be used to construct
    #: `.instance_name` which is then visible in various places in system (ie.
    #: logs, top, ...)
    APPLICATION_NAME = '{{cookiecutter.project_slug}}'

    #: UUID of currently running app server.
    #: Used to distinguish different app instances running on the same machine
    #: at the same time
    APPLICATION_INSTANCE_UUID = uuid.uuid4()

    #: Resolved value of $XDG_CONFIG_HOME (from https://specifications.freedesktop.org/basedir-spec/latest/)
    XDG_CONFIG_HOME = (
        os.path.join(os.environ.get('XDG_CONFIG_HOME'), APPLICATION_NAME)
        if os.environ.get('XDG_CONFIG_HOME') else None
    ) or os.path.join(current_user_home(), '.config', APPLICATION_NAME)

    #: Resolved value of $XDG_DATA_HOME (from https://specifications.freedesktop.org/basedir-spec/latest/)
    XDG_DATA_HOME = (
        os.path.join(os.environ.get('XDG_DATA_HOME'), APPLICATION_NAME)
        if os.environ.get('XDG_DATA_HOME') else None
    ) or os.path.join(current_user_home(), '.local', 'share', APPLICATION_NAME)

    #: Default tmp directory app will use if no config override is provided.
    DEFAULT_TEMP_DIR = os.path.join(tempfile.gettempdir(), '{{cookiecutter.project_slug}}.tmp')

    #: Root directory of application source code repo. Note that if we are
    #: running from within installed package this value will not point to
    #: anyhing meaningfull (see _IS_RUNNING_FROM_SOURCE)
    _REPO_ROOT = os.path.dirname(_SETUP_PY_PATH)

    #: Boolean signalling if currently running app server was started from
    #: within source code repo or from within pip installed package.
    _IS_RUNNING_FROM_SOURCE = os.path.isfile(_SETUP_PY_PATH)

    #: Override this in subclass if you want logging config to force
    #: one line of text per log event. Final effect of this is that new lines
    #: will be escaped in logs. Useful in production environments, less usefull
    #: in development environments.
    _FORCE_SINGLE_LINE_LOGS = True

    #: Override this in syslog if you want to force logging config to never
    #: configure syslog logging sink. This is usefull for development
    #: environments so we don't spam syslog no matter how does example
    #: logging_config.json look like.
    _FORCE_DISABLE_SYSLOG = False

    def __init__(self, cmdline_args: NamedTuple = None):
        self._errors = None
        self.cmdline_args = cmdline_args or namedtuple('CmdArguments', [])()
        self._logging_json = None
        self.app_config = {}    #: `dict` for contents of external config file(s)

    @property
    def instance_name(self) -> str:
        """Instance name is visible in logs and top/htop as process name.

        It is constructed from static value of APPLICATION_NAME and value of
        command line argument ``--process-name-suffix``.
        """
        return self.APPLICATION_NAME + (
            getattr(self.cmdline_args, 'process_name_suffix', '') or ''
        ).strip()

    @property
    def is_dry_run(self) -> bool:
        """State of ``--dry-run`` command line argument"""
        return getattr(self.cmdline_args, 'dry_run', False)

    @property
    def instance_tmp_dir_path(self) -> str:
        """
        Default base tmp directory. Either it is the one taken from external
        config or we query OS for it.
        """
        base_path = (
            (self.app_config or {}).get('tmp_dir_path')
            or self.DEFAULT_TEMP_DIR
        )
        return os.path.abspath(os.path.join(
            base_path, self.instance_name, self.APPLICATION_INSTANCE_UUID.hex
        ))

    @property
    @abstractmethod
    def filelog_abspath(self) -> str:
        """Absolute path to application's log file."""
        pass

    @property
    @abstractmethod
    def config_file_abspaths(self) -> List[str]:
        """
        List of absolute paths to all config file locations that will be
        loaded.
        """
        pass

    @property
    @abstractmethod
    def logging_config_abspaths(self) -> List[str]:
        """Absolute path to application's logging config file."""
        pass

    @property
    def logging_json(self) -> dict:
        """
        Loaded and fully resolved logging config dict.
        """
        if not self._logging_json:
            self._load_logging_config()

            if self._is_filelog_enabled:
                self._logging_json['handlers']['file']['filename'] = \
                    self.filelog_abspath
            else:
                if 'file' in self._logging_json['handlers']:
                    del(self._logging_json['handlers']['file'])

            for formatter in self._logging_json['formatters'].values():
                formatter['format'] = formatter['format'].format(
                    service_name=self.instance_name
                )

                if (
                    not self._FORCE_SINGLE_LINE_LOGS
                    and 'SingleLine' in formatter.get('()', '')
                ):
                    if 'Color' in formatter.get('()', ''):
                        formatter['()'] = 'colorlog.ColoredFormatter'
                    else:
                        del formatter['()']

            for logger_cfg in self._logging_json['loggers'].values():
                if self._FORCE_DISABLE_SYSLOG:
                    if 'handlers' in logger_cfg:
                        logger_cfg['handlers'] = [
                            handler for handler in logger_cfg['handlers']
                            if handler != 'syslog'
                        ]

        return self._logging_json

    def _load_logging_config(self):
        if not self._logging_json:
            self._logging_json = {}
            for json_path in self.logging_config_abspaths:
                try:
                    with open(json_path, 'r') as f:
                        self._logging_json.update(json.load(f) or {})

                except (IOError, ValueError, FileNotFoundError):
                    pass

        if not self._logging_json:
            with open(resource_filename(
                Requirement("{{cookiecutter.project_slug}}"),
                "{{cookiecutter.project_slug}}/resources/logging_config.json"
            ), 'r') as f:
                self._logging_json = json.load(f)

    def load_and_validate(self):
        """Loads and validates external app config."""
        self.app_config = {}
        errors = {}

        for conf_file_path in self.config_file_abspaths:
            try:
                with open(conf_file_path, 'r') as f:
                    config_data = yaml.load(f)

            except yaml.YAMLError:
                raise

            except Exception:
                config_data = {}

            self.app_config.update(config_data)

        if self._is_filelog_enabled:
            try:
                silent_create_dirs(os.path.dirname(self.filelog_abspath))
                with open(self.filelog_abspath, 'a'):
                    pass
            except Exception as exception:
                errors[self.filelog_abspath] = \
                    "Unable to open log file for writing! {}".format(
                        str(exception)
                    )

        if not errors:
            dictConfig(self.logging_json)

        if errors:
            raise ImproperlyConfiguredError(errors)

        silent_create_dirs(self.instance_tmp_dir_path)

        logger = logging.getLogger(__name__)
        logger.debug(
            "Initialized and resolved config for %s: %s",
            self.instance_name, json.dumps({
                'instance_name': self.instance_name,
                'instance_uuid': str(self.APPLICATION_INSTANCE_UUID),
                'config_files': self.config_file_abspaths,
                'app_config': self.app_config,
                'logging_json': self.logging_json,
                'cmdline_args': (
                    self.cmdline_args._asdict() if self.cmdline_args else None
                ),
                'tmp_dir': self.instance_tmp_dir_path
            })
        )
        if self._is_filelog_enabled:
            logger.debug("Logging to: %s", self.filelog_abspath)
        else:
            logger.debug(
                "Was not configured to log to file, check syslog instead..."
            )

    @property
    def _is_filelog_enabled(self) -> bool:
        return (
            'file' in self.logging_json['handlers']
            and any(
                'file' in logger['handlers']
                for logger in self.logging_json['loggers'].values()
            )
        )
