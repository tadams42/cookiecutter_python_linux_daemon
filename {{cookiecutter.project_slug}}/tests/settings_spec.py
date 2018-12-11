import os

import pytest
import simplejson as json
from pkg_resources import Requirement, resource_filename

from {{cookiecutter.project_slug}}.settings import ENVIRONMENTS, ImproperlyConfiguredError


class DescribeDevelopmentConfigLoader:
    def it_resolves_to_correct_default_config_paths(self):
        cfg = ENVIRONMENTS["development"]()
        # Prevent logging config from loading
        cfg._logging_json = {"handlers": {"file": {"filename": None}}}

        cfg._IS_RUNNING_FROM_SOURCE = True
        assert cfg.config_file_abspaths == [
            os.path.join(cfg._REPO_ROOT, "config", "development.yaml")
        ]
        assert cfg.filelog_abspath == os.path.join(
            cfg._REPO_ROOT, "log", "development.log"
        )
        assert cfg.logging_config_abspaths == [
            os.path.join(cfg._REPO_ROOT, "config", "logging_config.json")
        ]

        cfg._IS_RUNNING_FROM_SOURCE = False
        assert cfg.config_file_abspaths == [
            resource_filename(
                Requirement.parse("{{cookiecutter.project_slug}}"),
                "{{cookiecutter.project_slug}}/resources/development.yaml",
            )
        ]
        assert cfg.filelog_abspath == os.path.join(
            cfg.DEFAULT_TEMP_DIR, "development.log"
        )
        assert cfg.logging_config_abspaths == [
            resource_filename(
                Requirement.parse("{{cookiecutter.project_slug}}"),
                "{{cookiecutter.project_slug}}/resources/logging_config.json",
            )
        ]

    def it_accepts_absolute_paths_for_cmdline_arguments(self, mocker):
        absolute_paths = mocker.Mock()
        absolute_paths.config_file_path = "/absolute/path/config_file.yaml"
        absolute_paths.log_file_path = "/absolute/path/log_file.log"
        absolute_paths.logging_config_path = "/absolute/path/logging_config.json"

        cfg = ENVIRONMENTS["development"](absolute_paths)
        # Prevent logging config from loading
        cfg._logging_json = {"handlers": {"file": {"filename": None}}}

        cfg._IS_RUNNING_FROM_SOURCE = True
        assert cfg.config_file_abspaths == [absolute_paths.config_file_path]
        assert cfg.filelog_abspath == absolute_paths.log_file_path
        assert cfg.logging_config_abspaths == [absolute_paths.logging_config_path]

        cfg._IS_RUNNING_FROM_SOURCE = False
        assert cfg.config_file_abspaths == [absolute_paths.config_file_path]
        assert cfg.filelog_abspath == absolute_paths.log_file_path
        assert cfg.logging_config_abspaths == [absolute_paths.logging_config_path]

        cfg = ENVIRONMENTS["development"]()
        cfg._logging_json = {"handlers": {"file": {"filename": "/foo/bar.json"}}}
        assert cfg.filelog_abspath == "/foo/bar.json"

    def it_raises_if_it_gets_relative_paths_for_cmdline_arguments(self, mocker):
        relative_paths = mocker.Mock()
        relative_paths.config_file_path = "relative/path/config_file.yaml"
        relative_paths.log_file_path = "relative/path/log_file.log"
        relative_paths.logging_config_path = "relative/path/logging_config.json"

        cfg = ENVIRONMENTS["development"](relative_paths)
        # Prevent logging config from loading
        cfg._logging_json = {"handlers": {"file": {"filename": None}}}

        cfg._IS_RUNNING_FROM_SOURCE = True
        with pytest.raises(ImproperlyConfiguredError):
            cfg.config_file_abspaths
        with pytest.raises(ImproperlyConfiguredError):
            cfg.logging_config_abspaths
        with pytest.raises(ImproperlyConfiguredError):
            cfg.filelog_abspath

        cfg._IS_RUNNING_FROM_SOURCE = False
        with pytest.raises(ImproperlyConfiguredError):
            cfg.config_file_abspaths
        with pytest.raises(ImproperlyConfiguredError):
            cfg.logging_config_abspaths
        with pytest.raises(ImproperlyConfiguredError):
            cfg.filelog_abspath


class DescribeTestConfigLoader:
    def it_resolves_to_correct_default_config_paths(self):
        cfg = ENVIRONMENTS["test"]()
        # Prevent logging config from loading
        cfg._logging_json = {"handlers": {"file": {"filename": None}}}

        cfg._IS_RUNNING_FROM_SOURCE = True
        assert cfg.config_file_abspaths == [
            os.path.join(cfg._REPO_ROOT, "config", "test.yaml")
        ]
        assert cfg.filelog_abspath == os.path.join(cfg._REPO_ROOT, "log", "test.log")
        assert cfg.logging_config_abspaths == [
            os.path.join(cfg._REPO_ROOT, "config", "logging_config.json")
        ]

        cfg._IS_RUNNING_FROM_SOURCE = False
        assert cfg.config_file_abspaths == [
            resource_filename(
                Requirement.parse("{{cookiecutter.project_slug}}"), "{{cookiecutter.project_slug}}/resources/test.yaml"
            )
        ]
        assert cfg.filelog_abspath == os.path.join(cfg.DEFAULT_TEMP_DIR, "test.log")
        assert cfg.logging_config_abspaths == [
            resource_filename(
                Requirement.parse("{{cookiecutter.project_slug}}"),
                "{{cookiecutter.project_slug}}/resources/logging_config.json",
            )
        ]

    def it_accepts_absolute_paths_for_cmdline_arguments(self, mocker):
        absolute_paths = mocker.Mock()
        absolute_paths.config_file_path = "/absolute/path/config_file.yaml"
        absolute_paths.log_file_path = "/absolute/path/log_file.log"
        absolute_paths.logging_config_path = "/absolute/path/logging_config.json"

        cfg = ENVIRONMENTS["test"](absolute_paths)
        # Prevent logging config from loading
        cfg._logging_json = {"handlers": {"file": {"filename": None}}}

        cfg._IS_RUNNING_FROM_SOURCE = True
        assert cfg.config_file_abspaths == [absolute_paths.config_file_path]
        assert cfg.filelog_abspath == absolute_paths.log_file_path
        assert cfg.logging_config_abspaths == [absolute_paths.logging_config_path]

        cfg._IS_RUNNING_FROM_SOURCE = False
        assert cfg.config_file_abspaths == [absolute_paths.config_file_path]
        assert cfg.filelog_abspath == absolute_paths.log_file_path
        assert cfg.logging_config_abspaths == [absolute_paths.logging_config_path]

        cfg = ENVIRONMENTS["test"]()
        cfg._logging_json = {"handlers": {"file": {"filename": "/foo/bar.json"}}}
        assert cfg.filelog_abspath == "/foo/bar.json"

    def it_raises_if_it_gets_relative_paths_for_cmdline_arguments(self, mocker):
        relative_paths = mocker.Mock()
        relative_paths.config_file_path = "relative/path/config_file.yaml"
        relative_paths.log_file_path = "relative/path/log_file.log"
        relative_paths.logging_config_path = "relative/path/logging_config.json"

        cfg = ENVIRONMENTS["test"](relative_paths)
        # Prevent logging config from loading
        cfg._logging_json = {"handlers": {"file": {"filename": None}}}

        cfg._IS_RUNNING_FROM_SOURCE = True
        with pytest.raises(ImproperlyConfiguredError):
            cfg.config_file_abspaths
        with pytest.raises(ImproperlyConfiguredError):
            cfg.logging_config_abspaths
        with pytest.raises(ImproperlyConfiguredError):
            cfg.filelog_abspath

        cfg._IS_RUNNING_FROM_SOURCE = False
        with pytest.raises(ImproperlyConfiguredError):
            cfg.config_file_abspaths
        with pytest.raises(ImproperlyConfiguredError):
            cfg.logging_config_abspaths
        with pytest.raises(ImproperlyConfiguredError):
            cfg.filelog_abspath


class DescribeProductionConfigLoader:
    def it_resolves_to_correct_default_config_paths(self, mocker):
        cfg = ENVIRONMENTS["production"]()
        # Prevent logging config from loading
        cfg._logging_json = {"handlers": {"file": {"filename": None}}}

        cfg._IS_RUNNING_FROM_SOURCE = True
        assert cfg.config_file_abspaths == [
            "/etc/{{cookiecutter.project_slug}}/production.yaml",
            "/etc/{{cookiecutter.project_slug}}/production.yml",
            "/etc/{{cookiecutter.project_slug}}/app.yaml",
            "/etc/{{cookiecutter.project_slug}}/app.yml",
            os.path.join(cfg.XDG_CONFIG_HOME, "production.yaml"),
            os.path.join(cfg.XDG_CONFIG_HOME, "production.yml"),
            os.path.join(cfg.XDG_CONFIG_HOME, "app.yaml"),
            os.path.join(cfg.XDG_CONFIG_HOME, "app.yml"),
        ]
        assert cfg.filelog_abspath == os.path.join(cfg.XDG_DATA_HOME, "production.log")
        assert cfg.logging_config_abspaths == [
            "/etc/{{cookiecutter.project_slug}}/logging_config.json",
            os.path.join(cfg.XDG_CONFIG_HOME, "logging_config.json"),
        ]

        cfg._IS_RUNNING_FROM_SOURCE = False
        cfg._logging_json = {"handlers": {"file": {"filename": None}}}
        assert cfg.config_file_abspaths == [
            "/etc/{{cookiecutter.project_slug}}/production.yaml",
            "/etc/{{cookiecutter.project_slug}}/production.yml",
            "/etc/{{cookiecutter.project_slug}}/app.yaml",
            "/etc/{{cookiecutter.project_slug}}/app.yml",
            os.path.join(cfg.XDG_CONFIG_HOME, "production.yaml"),
            os.path.join(cfg.XDG_CONFIG_HOME, "production.yml"),
            os.path.join(cfg.XDG_CONFIG_HOME, "app.yaml"),
            os.path.join(cfg.XDG_CONFIG_HOME, "app.yml"),
        ]
        assert cfg.filelog_abspath == os.path.join(cfg.XDG_DATA_HOME, "production.log")
        assert cfg.logging_config_abspaths == [
            "/etc/{{cookiecutter.project_slug}}/logging_config.json",
            os.path.join(cfg.XDG_CONFIG_HOME, "logging_config.json"),
        ]

    def it_resolves_to_correct_config_paths_when_relative_override_given(self, mocker):
        cmdline_args = mocker.Mock()
        cmdline_args.config_file_path = "relative/path/config_file.yaml"
        cmdline_args.log_file_path = "relative/path/log_file.log"
        cmdline_args.logging_config_path = "relative/path/logging_config.json"

        cfg = ENVIRONMENTS["production"](cmdline_args)
        # Prevent logging config from loading
        cfg._logging_json = {"handlers": {"file": {"filename": None}}}

        cfg._IS_RUNNING_FROM_SOURCE = True
        assert cfg.config_file_abspaths == [
            os.path.join(cfg._REPO_ROOT, cmdline_args.config_file_path)
        ]
        assert cfg.filelog_abspath == os.path.join(
            cfg._REPO_ROOT, cmdline_args.log_file_path
        )
        assert cfg.logging_config_abspaths == [
            os.path.join(cfg._REPO_ROOT, cmdline_args.logging_config_path)
        ]

        cfg._IS_RUNNING_FROM_SOURCE = False
        cfg._logging_json = {"handlers": {"file": {"filename": None}}}
        assert cfg.config_file_abspaths == [
            os.path.join(cfg.XDG_CONFIG_HOME, cmdline_args.config_file_path)
        ]
        assert cfg.filelog_abspath == os.path.join(
            cfg.XDG_DATA_HOME, cmdline_args.log_file_path
        )
        assert cfg.logging_config_abspaths == [
            os.path.join(cfg.XDG_CONFIG_HOME, cmdline_args.logging_config_path)
        ]

        cfg = ENVIRONMENTS["production"]()

        cfg._IS_RUNNING_FROM_SOURCE = True
        cfg._logging_json = {"handlers": {"file": {"filename": "foo/bar.json"}}}
        assert cfg.filelog_abspath == os.path.join(cfg._REPO_ROOT, "foo/bar.json")

        cfg._IS_RUNNING_FROM_SOURCE = False
        cfg._logging_json = {"handlers": {"file": {"filename": "foo/bar.json"}}}
        assert cfg.filelog_abspath == os.path.join(cfg.XDG_DATA_HOME, "foo/bar.json")

    def it_resolves_to_correct_config_paths_when_absolute_override_given(self, mocker):
        cmdline_args = mocker.Mock()
        cmdline_args.config_file_path = "/absolute/path/config_file.yaml"
        cmdline_args.log_file_path = "/absolute/path/log_file.log"
        cmdline_args.logging_config_path = "/absolute/path/logging_config.json"

        cfg = ENVIRONMENTS["production"](cmdline_args)
        # Prevent logging config from loading
        cfg._logging_json = {"handlers": {"file": {"filename": None}}}

        cfg._IS_RUNNING_FROM_SOURCE = True
        assert cfg.config_file_abspaths == [cmdline_args.config_file_path]
        assert cfg.filelog_abspath == cmdline_args.log_file_path
        assert cfg.logging_config_abspaths == [cmdline_args.logging_config_path]

        cfg._IS_RUNNING_FROM_SOURCE = False
        cfg._logging_json = {"handlers": {"file": {"filename": None}}}
        assert cfg.config_file_abspaths == [cmdline_args.config_file_path]
        assert cfg.filelog_abspath == cmdline_args.log_file_path
        assert cfg.logging_config_abspaths == [cmdline_args.logging_config_path]

        cfg = ENVIRONMENTS["production"]()

        cfg._IS_RUNNING_FROM_SOURCE = True
        cfg._logging_json = {"handlers": {"file": {"filename": "/foo/bar.json"}}}
        assert cfg.filelog_abspath == os.path.join("/foo/bar.json")

        cfg._IS_RUNNING_FROM_SOURCE = False
        cfg._logging_json = {"handlers": {"file": {"filename": "/foo/bar.json"}}}
        assert cfg.filelog_abspath == os.path.join("/foo/bar.json")

    def it_loads_bundled_loging_config_if_no_external_files_exist(self, mocker):
        mocker.patch.object(
            ENVIRONMENTS["production"],
            "logging_config_abspaths",
            new_callable=mocker.PropertyMock,
            return_value=["/foo"],
        )
        cfg = ENVIRONMENTS["production"]()

        with open(
            resource_filename(
                Requirement("{{cookiecutter.project_slug}}"),
                "{{cookiecutter.project_slug}}/resources/logging_config.json",
            ),
            "r",
        ) as f:
            expected = json.load(f)

        assert cfg.logging_config_abspaths == ["/foo"]
        cfg._load_logging_config()
        assert cfg._logging_json == expected
