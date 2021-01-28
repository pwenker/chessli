import subprocess
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

from rich import print
from rich.console import Console
from rich.progress import track

from chessli import ChessliPaths
from chessli.games import Game
from chessli.openings import Opening
from chessli.utils import in_bold

console = Console()


class AnkifyError(RuntimeError):
    """
    Could not ankify. Have you set up `apy` correctly?
    """


def ankify_with_apy(
    file_path: Path, apy_header: str, md_notes: List[str], export_only: bool,
) -> None:
    md = f"{apy_header}"
    for md_note in md_notes:
        md += f"{md_note}\n\n"
    file_path.write_text(md)

    if export_only:
        print(f"Successfully exported mistakes to [bold]{file_path}[/bold].")
    else:
        try:
            subprocess.run(["apy", "add-from-file", file_path], input=b"n")
        except Exception as e:
            raise AnkifyError(e)


def ankify_games(
    games: List[Game], chessli_paths: ChessliPaths, export_only: bool
) -> None:
    for game in track(games, description="Ankifying your mistakes...\n"):
        num_mistakes = len(game.mistakes)
        print(
            f"Found [bold][red]{num_mistakes}[/red][/bold] mistakes in the game {in_bold(game.name)}."
        )
        if num_mistakes == 0:
            continue
        mistake_file_path = (chessli_paths.mistakes_dir / game.name).with_suffix(".md")

        apy_header = "model: Chessli Games\ntags: chess::game_analysis\ndeck: Chessli::games\nmarkdown: False\n\n"

        ankify_with_apy(
            file_path=mistake_file_path,
            apy_header=apy_header,
            md_notes=[mistake.md for mistake in game.mistakes],
            export_only=export_only,
        )


def ankify_openings(games=List[Game], export_only: bool = True):
    for game in games:
        if game.opening.exists():
            console.log(
                f"Ignoring {in_bold(game.opening.name)}'. You already know that opening :)"
            )
        else:
            console.log(f"Storing opening: {in_bold(game.opening.name)}")
            game.opening.store()
            if export_only:
                continue
            console.log(f"Ankifying opening: {in_bold(game.opening.name)}")
            game.opening.ankify()
