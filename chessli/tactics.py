import json
from dataclasses import dataclass
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path
from typing import Any, List, Set

import chess
import pandas as pd
from omegaconf import DictConfig
from rich.console import Console
from rich.table import Table

from chessli import ChessliPaths, users_client, utils
from chessli.enums import PuzzleDBSource
from chessli.rich_logging import log
from chessli.utils import import_to_anki_via_apy, in_bold

console = Console()


@dataclass
class PuzzleFetcherMixin:
    config: DictConfig
    paths: ChessliPaths

    def fetch_puzzle_activity(self):
        log.info(f"Fetching new puzzle activity...")
        puzzle_activity = list(users_client.get_puzzle_activity())
        return puzzle_activity

    def read_lichess_puzzle_database(self) -> pd.DataFrame:
        column_names = "PuzzleId,FEN,Moves,Rating,RatingDeviation,Popularity,NbPlays,Themes,GameUrl".split(
            ","
        )
        if self.config.db_source == PuzzleDBSource.remote:
            url = "https://database.lichess.org/lichess_db_puzzle.csv.bz2"
            log.info(
                f"Trying to read the most up-to-date lichess puzzle database from {url}. This may take a few seconds..."
            )
            puzzle_df = pd.read_csv(url, names=column_names, compression="bz2")
        elif self.config.db_source == PuzzleDBSource.local:
            puzzle_db_path = self.paths.tactics_dir / "lichess_db_puzzle.csv"
            log.info(
                f"Trying to read the lichess puzzle database from {puzzle_db_path}."
            )
            puzzle_df = pd.read_csv(puzzle_db_path, names=column_names)
        else:
            raise NotImplementedError(
                f"Unknown puzzle database source {self.config.db_source}"
            )
        return puzzle_df


@dataclass
class TacticsManager(PuzzleFetcherMixin, object):
    config: DictConfig
    paths: ChessliPaths

    def get_puzzle_ids_path(self) -> Path:
        puzzles_ids_path = self.paths.tactics_dir / "played_puzzles_ids.json"
        puzzles_ids_path.touch(exist_ok=True)
        return puzzles_ids_path

    def read_puzzle_ids(self) -> List:
        puzzle_ids_path = self.get_puzzle_ids_path()
        try:
            with puzzle_ids_path.open("r") as fp:
                old_puzzle_ids = json.load(fp)
        except (FileNotFoundError, JSONDecodeError):
            old_puzzle_ids = []
        return old_puzzle_ids

    def store_puzzle_ids(self, puzzle_ids: List[str]) -> None:
        puzzle_ids_path = self.get_puzzle_ids_path()
        with puzzle_ids_path.open("w") as fp:
            json.dump(puzzle_ids, fp)

    def _get_ids_from_puzzle_activity(
        self, puzzle_activity: List[Any], new_only: bool = True,
    ) -> List[str]:
        puzzle_ids = [puzzle["id"] for puzzle in puzzle_activity]
        if new_only:
            old_puzzle_ids = self.read_puzzle_ids()
            new_puzzle_ids = set(puzzle_ids) - set(old_puzzle_ids)
            log.info(f"There are {len(new_puzzle_ids)} new puzzles!")
            return new_puzzle_ids
        else:
            return puzzle_ids

    def print_new_puzzles(self) -> None:
        puzzle_activity = self.fetch_puzzle_activity()
        puzzle_ids = self._get_ids_from_puzzle_activity(puzzle_activity)
        if not puzzle_ids:
            return None
        puzzles_df = self.read_lichess_puzzle_database()
        new_puzzles_df = self._extract_new_puzzles(puzzle_ids, puzzles_df)

        table = Table(
            *list(new_puzzles_df),
            title=f"Played Puzzles ({len(new_puzzles_df)}) :fire:",
        )
        for idx, puzzle in new_puzzles_df.iterrows():
            table.add_row(*[str(val) for val in puzzle.values])

        console.print(table)

    def _extract_new_puzzles(self, puzzle_ids, df: pd.DataFrame) -> pd.DataFrame:
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

    def update_stored_puzzle_ids(self, puzzle_ids) -> None:
        old_puzzle_ids = self.read_puzzle_ids()
        if not old_puzzle_ids:
            old_puzzle_ids = []
        puzzle_ids = set(puzzle_ids) | set(old_puzzle_ids)
        self.store_puzzle_ids(list(puzzle_ids))

    def ankify_puzzles(self) -> None:
        if self.config.new:
            puzzle_activity = self.fetch_puzzle_activity()
            puzzle_ids = self._get_ids_from_puzzle_activity(puzzle_activity)
        else:
            puzzle_ids = self.read_puzzle_ids()

        if not puzzle_ids:
            log.info(
                f"There are no new puzzles to be ankified! Time to play some! :fire:"
            )
            return

        puzzles_df = self.read_lichess_puzzle_database()
        new_puzzles_df = self._extract_new_puzzles(puzzle_ids, puzzles_df)

        time_stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        apy_str = self.puzzle_df_to_apy_md(new_puzzles_df)
        last_puzzles_path = self.paths.tactics_dir / f"puzzle_export_{time_stamp}.md"

        last_puzzles_path.write_text(apy_str)

        new_puzzles_df.to_csv(
            index=False, path_or_buf=last_puzzles_path.with_suffix(".csv")
        )

        log.info(
            f"Exported played puzzles to {in_bold(last_puzzles_path)} and {in_bold(last_puzzles_path.with_suffix('.csv'))}"
        )

        if not self.config.export_only:
            log.info(f"Firing up 'apy' to import the new puzzles into anki.")
            import_to_anki_via_apy(file_path=last_puzzles_path)

        self.update_stored_puzzle_ids(puzzle_ids)

    @staticmethod
    def puzzle_df_to_apy_md(df: pd.DataFrame) -> str:
        md = ""
        header = "model: Chessli Tactics\ntags: chess::tactics\ndeck: Chessli::tactics\nmarkdown: False\n\n"
        md += header
        for idx, row in df.iterrows():
            md += "# Note\n"
            for key, value in row.items():
                md += f"## {key}\n"
                md += f"{value}\n"
        return md
