from typing import Optional

import typer
from omegaconf import OmegaConf
from rich import print
from rich.console import Console
from rich.table import Table

from chessli.enums import SinceEnum
from chessli.games import GameManager
from chessli.openings import ECOVolume, list_known_openings
from chessli.utils import convert_since_enum_to_millis, create_config_from_options

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context,):
    """Show and ankify chess openings"""

    ctx.params = ctx.parent.params
    print(f":fire: [blue][bold]CHESSLI OPENINGS[/bold][/blue] :fire:", end="\n\n")


@app.command()
def ls(
    ctx: typer.Context,
    eco: Optional[ECOVolume] = typer.Option(
        default=None, help="Limit the shown openings to specific ECO volume"
    ),
):
    """List your played openings"""
    config = create_config_from_options({**ctx.parent.params, **ctx.params})
    list_known_openings(eco, config)


@app.command()
def ankify(
    ctx: typer.Context,
    new_openings_only: bool = typer.Option(True, help="Only ankify new openings"),
    since: Optional[SinceEnum] = SinceEnum.last_time,
):
    """Parse your games to find new openings and create Anki cards"""
    config = create_config_from_options({**ctx.parent.params, **ctx.params})
    last_fetch_config = OmegaConf.load(config.paths.configs.fetching)
    config.since = convert_since_enum_to_millis(since, last_fetch_config)
    game_manager = GameManager(config)

    if new_openings_only:
        new_games = game_manager.fetch_games()
        games = new_games
    else:
        games = game_manager.games

    for game in games:
        if not game.opening.exists():
            # console.log(f"Storing opening: '{game.opening.name}'")
            game.opening.store()
            console.log(f"Ankifying opening: '{game.opening.name}'")
            game.opening.ankify()
        else:
            console.log(
                f"Ignoring '{game.opening.name}'. You already know that opening :)"
            )


if __name__ == "__main__":
    app()
