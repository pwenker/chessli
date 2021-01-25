import json
import subprocess
from pathlib import Path
from typing import Any, List, Set

import chess
import pandas as pd
from rich.console import Console
from rich.table import Table

from chessli import utils
from chessli.enums import PuzzleDBSource
from chessli.user import users_client

console = Console()


def fetch_puzzle_activity():
    console.log(f"Fetching new puzzle activity...")
    puzzle_activity = list(users_client.get_puzzle_activity())
    return puzzle_activity


def read_puzzle_ids(config) -> List:
    puzzle_ids_path = get_puzzle_ids_path(config)
    try:
        with puzzle_ids_path.open("r") as fp:
            old_puzzle_ids = json.load(fp)
    except FileNotFoundError:
        old_puzzle_ids = []
    return old_puzzle_ids


def store_puzzle_ids(config, puzzle_ids: List[str]) -> None:
    puzzle_ids_path = get_puzzle_ids_path(config)
    with puzzle_ids_path.open("w") as fp:
        json.dump(puzzle_ids, fp)


def get_ids_from_puzzle_activity(
    config, puzzle_activity: List[Any], new_only: bool = True, verbose=True
) -> List[str]:
    puzzle_ids = [puzzle["id"] for puzzle in puzzle_activity]
    if new_only:
        old_puzzle_ids = read_puzzle_ids(config)
        new_puzzle_ids = set(puzzle_ids) - set(old_puzzle_ids)
        if verbose:
            console.log(f"There are {len(new_puzzle_ids)} new puzzles!")
        return new_puzzle_ids
    else:
        return puzzle_ids


def get_puzzle_ids_path(config) -> Path:
    puzzle_path = config.paths.puzzles.value
    puzzle_path.mkdir(exist_ok=True)
    puzzles_ids_path = puzzle_path / "played_puzzles_ids.json"
    return puzzles_ids_path


def update_stored_puzzle_ids(puzzle_ids, config) -> None:
    old_puzzle_ids = read_puzzle_ids(config)
    if not old_puzzle_ids:
        old_puzzle_ids = []
    puzzle_ids = set(puzzle_ids) | set(old_puzzle_ids)
    store_puzzle_ids(config, list(puzzle_ids))


def read_lichess_puzzle_database(config) -> pd.DataFrame:
    column_names = "PuzzleId,FEN,Moves,Rating,RatingDeviation,Popularity,NbPlays,Themes,GameUrl".split(
        ","
    )
    if config.db_source == PuzzleDBSource.remote:
        url = "https://database.lichess.org/lichess_db_puzzle.csv.bz2"
        console.log(
            f"Trying read the most up-to-date lichess puzzle database from {url}. This may take a while..."
        )
        puzzle_df = pd.read_csv(url, names=column_names, compression="bz2")
    elif config.db_source == PuzzleDBSource.local:
        puzzle_db_path = config.paths.puzzles.value / "lichess_db_puzzle.csv"
        console.log(f"Trying read the lichess puzzle database from {puzzle_db_path}")
        puzzle_df = pd.read_csv(puzzle_db_path, names=column_names)
    else:
        raise NotImplementedError(f"Unknown puzzle database source {config.db_source}")
    return puzzle_df


def extract_new_puzzles(puzzle_ids, df: pd.DataFrame) -> pd.DataFrame:
    new_puzzles = df.loc[df["PuzzleId"].isin(puzzle_ids)]

    def assign_san_moves(df: pd.DataFrame) -> List[str]:
        """We need to do some transformation to get a compatible move list"""
        move_list = []
        for idx, row in df.iterrows():
            san_move = chess.Board(row["FEN"]).variation_san(
                [chess.Move.from_uci(m) for m in row["Moves"].split()]
            )
            move_list.append(san_move)

        return move_list

    pd.options.mode.chained_assignment = None  # Suppress false positive warning
    new_puzzles["Move List"] = assign_san_moves(new_puzzles)
    return new_puzzles


def print_new_puzzles(config, puzzle_activity) -> None:
    puzzle_ids = get_ids_from_puzzle_activity(config, puzzle_activity)
    puzzles_df = read_lichess_puzzle_database(config)
    new_puzzles_df = extract_new_puzzles(puzzle_ids, puzzles_df)

    table = Table(
        *list(new_puzzles_df), title=f"Played Puzzles ({len(new_puzzles_df)}) :fire:"
    )
    for idx, puzzle in new_puzzles_df.iterrows():
        table.add_row(*[str(val) for val in puzzle.values])

    console.print(table)


def ankify_puzzles(puzzle_ids: Set[str], config) -> None:

    puzzles_df = read_lichess_puzzle_database(config)
    new_puzzles_df = extract_new_puzzles(puzzle_ids, puzzles_df)

    apy_str = utils.df_to_apy(new_puzzles_df)

    last_puzzles_path = config.paths.puzzles.value / "last_ankified_puzzles.md"
    last_puzzles_path.write_text(apy_str)

    console.log(f"Firing up 'apy' to import the new puzzles into anki.")
    subprocess.run(["apy", "add-from-file", last_puzzles_path], input=b"n")
