from typing import Callable, Dict, List, Optional, Set, Tuple, Union

import typer
from omegaconf import OmegaConf
from rich import print
from rich.console import Console
from rich.progress import track

from chessli.enums import PerfType, SinceEnum
from chessli.games import GamesFetcher, GamesReader
from chessli.utils import (
    ankify_with_apy,
    convert_since_enum_to_millis,
    create_config_from_options,
)

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context,):
    """Fetch, store, show and ankify games and mistakes"""
    ctx.params = ctx.parent.params
    print(f":fire: [blue][bold]Chessli Games[/bold][/blue] :fire:", end="\n\n")


@app.command()
def ls(ctx: typer.Context):
    """List your games"""
    chessli_paths = ctx.parent.params["paths"]
    cli_params = {**ctx.parent.params, **ctx.params}
    cli_config = create_config_from_options(cli_params)
    games_reader = GamesReader(chessli_paths, cli_config)
    games_reader.ls()
    games = games_reader.games
    __import__("pdb").set_trace()


@app.command()
def fetch(
    ctx: typer.Context,
    verbose: int = typer.Option(1, "--verbose", "-v", count=True),
    store: bool = typer.Option(False, help="Select if fetched games should be stored"),
    perf_type: Optional[PerfType] = typer.Option(
        None, help="Filter fetching of games to the selected `perf_type`"
    ),
    since_enum: SinceEnum = typer.Option(
        SinceEnum.last_time,
        "--since",
        help="Filter fetching of games to those played since `since`",
    ),
    max: Optional[int] = typer.Option(10, help="Limit fetching of games to `max`",),
):
    """Fetch games from lichess"""
    chessli_paths = ctx.parent.params["paths"]
    cli_params = {**ctx.parent.params, **ctx.params}

    cli_config = create_config_from_options(cli_params)
    cli_config["since_millis"] = convert_since_enum_to_millis(
        since_enum, chessli_paths.user_config.last_fetch_time
    )

    games_fetcher = GamesFetcher(chessli_paths, cli_config)
    new_games = games_fetcher.fetch_games()


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
    last_fetch_config = OmegaConf.load(config.paths.user_config.fetching)
    config.since = convert_since_enum_to_millis(since, last_fetch_config)

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


@app.command()
def export(
    ctx: typer.Context,
    new_games_only: bool = typer.Option(
        True, help="Fetch new games and only ankify those"
    ),
    since: Optional[SinceEnum] = SinceEnum.last_time,
):
    """Parse your games to find mistakes and create Anki cards"""

    config = create_config_from_options({**ctx.parent.params, **ctx.params})
    last_fetch_config = OmegaConf.load(config.paths.user_config.fetching)
    config.since = convert_since_enum_to_millis(since, last_fetch_config)

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
