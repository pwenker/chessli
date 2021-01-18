from typing import Optional

import typer
from omegaconf import OmegaConf
from rich import print
from rich.console import Console
from rich.progress import track

from chessli.enums import PerfType, SinceEnum
from chessli.games import GameManager
from chessli.utils import (
    ankify_with_apy,
    convert_since_enum_to_millis,
    create_config_from_options,
)

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
):
    """Fetch and show games & find and ankify mistakes"""
    ctx.params = ctx.parent.params
    print(f":fire: [blue][bold]Chessli Games[/bold][/blue] :fire:", end="\n\n")


@app.command()
def ls(ctx: typer.Context):
    """List your games"""
    config = create_config_from_options({**ctx.parent.params, **ctx.params})
    game_names = sorted([f.stem for f in config.paths.games.value.glob("*/*.pgn")])
    print(game_names)


@app.command()
def fetch(
    ctx: typer.Context,
    perf_type: Optional[PerfType] = typer.Option(
        None, help="Select which type of games should be fetched"
    ),
    since: Optional[SinceEnum] = typer.Option(
        SinceEnum.last_time, help="Select to fetch all games played 'since'"
    ),
):
    """Fetch games from Lichess"""
    if perf_type is not None:
        raise NotImplementedError(
            f"Choosing games of a particular PerfType is not yet implemented"
        )

    config = create_config_from_options({**ctx.parent.params, **ctx.params})
    last_fetch_config = OmegaConf.load(config.paths.configs.fetching)
    config.since = convert_since_enum_to_millis(since, last_fetch_config)
    game_manager = GameManager(config)
    game_manager.fetch_games()


@app.command()
def ankify(
    ctx: typer.Context,
    new_games_only: bool = typer.Option(
        True, help="Fetch new games and only ankify those"
    ),
    since: Optional[SinceEnum] = SinceEnum.last_time,
):
    """Parse your games to find mistakes and create Anki cards"""
    config = create_config_from_options({**ctx.parent.params, **ctx.params})
    last_fetch_config = OmegaConf.load(config.paths.configs.fetching)
    config.since = convert_since_enum_to_millis(since, last_fetch_config)
    game_manager = GameManager(config)

    if new_games_only:
        new_games = game_manager.fetch_games()
        last_fetch_config = OmegaConf.load(config.paths.configs.fetching)
        games = new_games
    else:
        games = game_manager.games

    for game in track(games, description="Ankifying your mistakes..."):
        print(
            f"Found [bold][red]{len(game.mistakes())}[/red][/bold] mistakes in '{game.name}'."
        )
        mistake_folder = config.paths.mistakes.value
        mistake_folder.mkdir(parents=True, exist_ok=True)
        mistake_file_path = (mistake_folder / game.name).with_suffix(".md")

        apy_header = "model: Chessli Games\ntags: chess::game_analysis\ndeck: Chessli::games\nmarkdown: False\n\n"

        ankify_with_apy(
            file_path=mistake_file_path,
            apy_header=apy_header,
            md_notes=[mistake.md for mistake in game.mistakes()],
        )


if __name__ == "__main__":
    app()
