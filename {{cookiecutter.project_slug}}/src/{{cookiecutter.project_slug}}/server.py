import logging
import signal
import sys
import time
from typing import NamedTuple

import prctl

from . import __version__, settings
from .settings import SETTINGS

logger = logging.getLogger(__name__)


class Server:
    """
    Application server. Intended to be used as singleton. Runs main application
    thread, handles signals and makes sure everything starts up and shuts down
    cleanly.

    Arguments:
        environment: name of runtime environment (ie. 'test', 'development',
            'production')
        cmdline_args: parsed and validated command line arguments.
    """
    def __init__(self, environment: str, cmdline_args: NamedTuple = None):
        settings.init_module(environment, cmdline_args)
        prctl.set_proctitle(SETTINGS.instance_name)

    def before_startup(self):
        """Executed before main thread loop is started."""
        pass

    def startup(self):
        """Starts main thread loop."""
        logger.info(
            "Starting up '%s' (v%s) application server...",
            SETTINGS.instance_name,
            __version__,
        )

        for signame in ('SIGINT', 'SIGTERM', 'SIGHUP', 'SIGQUIT'):
            signal.signal(
                getattr(signal, signame), lambda signum, frame: self.shutdown(signame)
            )

        self.before_startup()

        while True:
            time.sleep(1)

    def before_shutdown(self):
        """Executed before main thread loop is terminated."""
        settings.cleanup_module()

    def shutdown(self, signame):
        """Terminates main thread loop."""
        logger.info(
            "Initiating shut down of '%s' application server...", SETTINGS.instance_name
        )

        self.before_shutdown()

        logger.info(
            "Application server '%s' was shut down. So Long, and Thanks for "
            "All the Fish!",
            SETTINGS.instance_name,
        )

        sys.exit(0)


def create_app(cmdline_args):
    """
    `.Server` factory.

    Arguments:
        cmdline_args(collections.NamedTuple): parsed command line
            arguments.
    """
    return Server(cmdline_args.environment, cmdline_args)
