import textwrap
from collections import namedtuple

import click
from click_help_colors import HelpColorsGroup

from ..settings import ENVIRONMENTS


def args_from_dict(**kwargs):
    return namedtuple('CmdArguments', (kwargs or {}).keys())(**(kwargs or {}))


_MAIN_HELP_TEXT = """
    {{cookiecutter.project_slug}} service.

    Application loads configuration in standard Linux way: it loads systemwide
    configuration first (if there is any) and then loads per-user config (from
    $XDG_CONFIG_HOME), replacing values from systemwide config.

    Config files are either default ones or explicitly specified on command
    line. The exact mechanism is as follows.

    \b
        1. application config file paths
            - value of {config_file_path} if one is provided
            - otherwise following locations are loaded
                - {etc_config_path}
                - {xdg_config_path}
        2. logging config JSON file path
            - value of {logging_config_path} if provided
            - otherwise following locations are loaded
                - {etc_log_config_path}
                - {xdg_log_config_path}

    In case no logging config path can be loaded, application will use
    default bundled logging config.

    Depending on logging config, application can log to stdout, file or syslog
    (or any combination of these three). If logging to file, log file path
    needs to be specified. This can be done by following:

    \b
        - value of {log_file_path} if provided
        - or value from logging config JSON if provided
        - or default value {default_log_file_path}

    If any of config values use relative paths, they are resolved into
    absolute ones like this:

    \b
        - if app is running from source repo, relative paths are resolved as
          relative to the repo root
        - if app is running from installed package, relative paths are resolved
          as relative to $XDG_CONFIG_HOME and $XDG_DATA_HOME
""".format(
    config_file_path=click.style('--config-file-path', fg='green'),
    logging_config_path=click.style('--logging-config-path', fg='green'),
    log_file_path=click.style('--log-file-path', fg='green'),

    etc_config_path=click.style('/etc/{{cookiecutter.project_slug}}/production.yaml', fg='red'),
    xdg_config_path=click.style('$XDG_CONFIG_HOME/{{cookiecutter.project_slug}}/production.yaml', fg='red'),
    etc_log_config_path=click.style('/etc/{{cookiecutter.project_slug}}/logging_config.json', fg='red'),
    xdg_log_config_path=click.style('$XDG_CONFIG_HOME/{{cookiecutter.project_slug}}/logging_config.json', fg='red'),

    default_log_file_path=click.style('$XDG_DATA_HOME/{{cookiecutter.project_slug}}/production.log', fg='red'),
)


@click.group(
    cls=HelpColorsGroup,
    help_headers_color='yellow', help_options_color='green',
    context_settings=dict(max_content_width=120),
    help=_MAIN_HELP_TEXT
)
@click.version_option()
@click.option(
    '-e', '--environment', default='development', show_default=True,
    type=click.Choice(ENVIRONMENTS.keys()),
    help="Config environment that will be used by application server."
)
@click.option(
    '-c', '--config-file-path', type=click.Path(), required=False,
    help="Optional path to application config file."
)
@click.option(
    '-l', '--log-file-path', type=click.Path(), required=False,
    help="Optional path to application log file."
)
@click.option(
    '--logging-config-path', type=click.Path(), required=False,
    help="Optional path to application logging config file."
)
@click.option(
    '--process-name-suffix', required=False,
    help=(textwrap.dedent("""
        Optional suffix that will be appended to running app's process name.
    """).replace('\n', ' ').strip())
)
@click.option(
    '--dry-run/--no-dry-run', default=False,
    show_default=True,
    help="Process everything but don't commit results."
)
@click.pass_context
def cli(ctx, **kwargs):
    # kwargs are parsed commandline parameters
    ctx.obj = args_from_dict(**kwargs)
