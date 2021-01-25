import typer
from rich import print

from chessli.enums import PuzzleDBSource
from chessli.tactics import (
    ankify_puzzles,
    fetch_puzzle_activity,
    get_ids_from_puzzle_activity,
    print_new_puzzles,
    read_puzzle_ids,
    update_stored_puzzle_ids,
)
from chessli.utils import create_config_from_options

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
    ctx.params = {**ctx.parent.params, **ctx.params}
    print(f":fire: [blue][bold]Chessli Tactics[/bold][/blue] :fire:", end="\n\n")


@app.command()
def ls(
    ctx: typer.Context,
    new: bool = typer.Option(
        True, "--new/--old", help="Select whether to fetch and list new puzzles only"
    ),
):
    """Print a pretty table of the newly played puzzles"""
    config = create_config_from_options({**ctx.parent.params, **ctx.params})
    if new:
        puzzle_activity = fetch_puzzle_activity()
        print_new_puzzles(config, puzzle_activity)
    else:
        puzzle_ids = read_puzzle_ids(config)
        print(f"{puzzle_ids}")


@app.command()
def ankify(
    ctx: typer.Context,
    fetch: bool = typer.Option(
        True, help="Select whether to fetch new puzzles before ankifying"
    ),
):
    """Optionally fetch new puzzles and ankify them"""
    config = create_config_from_options({**ctx.parent.params, **ctx.params})

    if fetch:
        puzzle_activity = fetch_puzzle_activity()
        print_new_puzzles(config, puzzle_activity)
        puzzle_ids = get_ids_from_puzzle_activity(
            config, puzzle_activity, verbose=False
        )
    else:
        puzzle_ids = read_puzzle_ids(config)

    if not puzzle_ids:
        print(f"There are no new puzzles to be ankified! Time to play some! :fire:")
    else:
        ankify_puzzles(puzzle_ids, config)
        update_stored_puzzle_ids(puzzle_ids, config)


if __name__ == "__main__":
    app()
