import click
import IPython
from click_help_colors import HelpColorsCommand

from ..server import create_app
from ..settings import SETTINGS
from .main import cli


@cli.command(cls=HelpColorsCommand)
@click.pass_context
def shell(ctx):
    """Starts application shell."""

    IPython.start_ipython(argv=[], user_ns={
        "app": create_app(ctx.obj),
        "SETTINGS": SETTINGS
    })
