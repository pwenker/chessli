from typing import Optional

import typer
from rich import print
from rich.console import Console

from chessli import default_user, generate_path_container
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
):
    if user is None:
        if default_user is None:
            console.log(
                f"You didn't select a user name, so obviously we default to using 'Magnus Carlsen'"
            )
            user = "DrNykterstein"
        else:
            user = default_user.strip()
        ctx.params["user"] = user
    ctx.params["paths"] = generate_path_container(user)


if __name__ == "__main__":
    app()
