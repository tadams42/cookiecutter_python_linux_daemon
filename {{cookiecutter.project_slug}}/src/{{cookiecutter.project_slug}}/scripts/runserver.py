import click
from click_help_colors import HelpColorsCommand

from ..server import create_app
from .main import cli


@cli.command(cls=HelpColorsCommand)
@click.pass_context
def runserver(ctx):
    """Starts application server."""
    # ctx.obj are parsed command line parameters from parent command
    app = create_app(ctx.obj)
    app.startup()
