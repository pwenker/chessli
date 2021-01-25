import sys
from typing import Optional

import typer
from rich import print
from rich.console import Console

from chessli import ChessliUserPaths, main_config
from chessli.cli import games as games_cli
from chessli.cli import lichess as lichess_cli
from chessli.cli import openings as openings_cli
from chessli.cli import tactics as tactics_cli

app = typer.Typer()
console = Console()


app.add_typer(openings_cli.app, name="openings")
app.add_typer(games_cli.app, name="games")
app.add_typer(lichess_cli.app, name="lichess")
app.add_typer(tactics_cli.app, name="tactics")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    user: Optional[str] = typer.Option(None, help="Select a user name"),
    show_config: bool = typer.Option(False, help="Show chessli configuration"),
):

    if user is None:
        if main_config.user is None:
            console.log(
                f"User name is missing!"
                f"Take a look at the documentation: https://pwenker.com/chessli/home/"
            )
            sys.exit(1)
        else:
            user = main_config.user

    ctx.params["user"] = user
    ctx.params["paths"] = ChessliUserPaths(user)

    if show_config:
        print(ctx.params["paths"])


if __name__ == "__main__":
    app()
