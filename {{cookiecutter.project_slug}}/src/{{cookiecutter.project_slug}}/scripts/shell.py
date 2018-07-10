import click
import IPython
from click_help_colors import HelpColorsCommand

from ..server import create_app
from .main import cli


@cli.command(cls=HelpColorsCommand)
@click.pass_context
def shell(ctx):
    """Starts application shell."""
    # ctx.obj are parsed command line parameters from parent command
    app = create_app(ctx.obj)
    IPython.embed()
