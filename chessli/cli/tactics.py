import typer
from rich import print

from chessli.enums import PuzzleDBSource
from chessli.tactics import TacticsManager
from chessli.utils import (
    as_title,
    create_config_from_options,
    extract_context_info,
    in_bold,
)

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    db_source: PuzzleDBSource = typer.Option(
        PuzzleDBSource.remote,
        help="Select where to get the lichess puzzle database from.",
    ),
):
    """Chessli Tactics & Puzzles"""
    ctx.params = {**ctx.params, **ctx.parent.params}
    print(f"{as_title('chessli tactics')}", end="\n\n")


@app.command()
def ls(
    ctx: typer.Context,
    new: bool = typer.Option(
        True, "--new/--old", help="Select whether to fetch and list new puzzles only"
    ),
):
    """Print a pretty table of the newly played puzzles"""
    chessli_paths, config = extract_context_info(ctx)
    tactics_manager = TacticsManager(config, chessli_paths)
    if new:
        tactics_manager.print_new_puzzles()
    else:
        puzzle_ids = tactics_manager.read_puzzle_ids()
        print(f"{puzzle_ids}")


@app.command()
def ankify(
    ctx: typer.Context,
    new: bool = typer.Option(
        True,
        "--new/--all",
        help="Select whether to only ankify new puzzles or all puzzles",
    ),
    export_only: bool = typer.Option(
        True,
        "--export-only/--directly",
        help="Select to only export the created anki cards",
    ),
):
    """Optionally fetch new puzzles and ankify them"""
    chessli_paths, config = extract_context_info(ctx)

    tactics_manager = TacticsManager(config, chessli_paths)
    tactics_manager.ankify_puzzles()


if __name__ == "__main__":
    app()
