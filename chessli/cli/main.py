import sys
from enum import Enum
from typing import Optional

import typer
from rich import print
from rich.console import Console

from chessli import ChessliPaths, __version__, main_config
from chessli.cli import games as games_cli
from chessli.cli import openings as openings_cli
from chessli.cli import stats as stats_cli
from chessli.cli import tactics as tactics_cli
from chessli.cli.option_callbacks import version_callback
from chessli.rich_logging import log
from chessli.utils import as_title, in_bold

app = typer.Typer()
console = Console()


app.add_typer(openings_cli.app, name="openings")
app.add_typer(games_cli.app, name="games")
app.add_typer(stats_cli.app, name="stats")
app.add_typer(tactics_cli.app, name="tactics")


class LogLevel(Enum):
    debug = 10
    info = 20
    warning = 30


def log_level_from_verbosity(v: int) -> LogLevel:
    return {1: LogLevel.warning, 2: LogLevel.info, 3: LogLevel.debug}.get(
        v, LogLevel.info
    )


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
    verbosity: int = typer.Option(
        2,
        "--verbose",
        "-v",
        count=True,
        help="Select verbosity level: Warning(-v), Info(-vv) Debug(-vvv), ",
    ),
    user: Optional[str] = typer.Option(None, help="Select a user name"),
    show_configs: bool = typer.Option(False, help="Show chessli configuration"),
    show_paths: bool = typer.Option(False, help="Show chessli paths"),
):
    f"""Chessli version {__version__}"""

    log_level = log_level_from_verbosity(verbosity).value
    log.setLevel(log_level)

    if main_config.token:
        log.debug(
            f"Chessli found your token. You'll be able to perform any request :fire:"
        )
    else:
        log.debug(
            f"Chessli did not found any lichess API token. You'll not be able to perform some requests."
        )

    if user is None:
        if main_config.user is None:
            console.log(
                f"You haven't chosen any username!\n Use `--user <your_username>`\n"
                f"Take a look at the documentation: https://pwenker.com/chessli/tutorial/ to learn how to set up a default username!"
            )
            sys.exit(1)
        else:
            user = main_config.user

    ctx.params["user"] = user
    ctx.params["paths"] = chessli_paths = ChessliPaths(user_name=user)

    if show_paths or log_level == LogLevel.debug:
        log.info(chessli_paths)

    if show_configs or log_level == LogLevel.debug:
        log.info(f"{in_bold('General Config')}")
        log.info(chessli_paths.main_config)
        log.info(f"{in_bold('User Config')}")
        log.info(chessli_paths.user_config)


if __name__ == "__main__":
    app()
