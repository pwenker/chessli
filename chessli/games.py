import collections
import io
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import chess.pgn
import chess.svg
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from rich import print
from rich.console import Console
from rich.progress import track
from rich.table import Table

from chessli import AnkifyError, ChessliPaths, berserk_client
from chessli.enums import Color
from chessli.mistakes import Mistake, MistakeFinderMixin, get_nag_name
from chessli.openings import Opening, OpeningExtractorMixin
from chessli.rich_logging import log
from chessli.utils import import_to_anki_via_apy, in_bold

console = Console()


games_client = berserk_client.games


@dataclass
class GamesFetcher:
    paths: ChessliPaths
    config: DictConfig

    def _print_games_table(self, counter: collections.Counter) -> None:
        games_table = self.counter_to_table(
            counter=counter,
            title="New Games :fire:",
            columns=["Game Type", "Number of Plays"],
        )
        console.log(games_table)

    def _print_openings_table(self, counter: collections.Counter) -> None:
        openings_table = self.counter_to_table(
            counter=counter,
            title="New Openings :fire:",
            columns=["Opening Name", "Number of Plays"],
        )
        console.log(openings_table)

    def _store_user_config(self) -> None:
        self.config.fetch_time = str(datetime.now())
        new_fetch_config = OmegaConf.create(
            {
                "since_millis": self.config.since_millis,
                "last_fetch_time": self.config.fetch_time,
            }
        )
        OmegaConf.save(config=new_fetch_config, f=self.paths.user_config_path)
        log.info(
            f"Updated the user config`s {in_bold('last_fetch_time')} with the current timestamp."
        )

    def _fetch_games_by_user(self) -> List:
        console.log(f"Fetching games of {in_bold(self.config.user)}.")
        games_by_user = []
        if self.config.perf_type is None:
            self.config.perf_type = [None]
        for perf_type in self.config.perf_type:
            if perf_type is not None:
                log.info(f"Fetching {in_bold(perf_type)} games...")
            for game in games_client.export_by_player(
                max=self.config.max,
                username=self.config.user,
                since=int(self.config.since_millis),
                perf_type=perf_type,
            ):
                games_by_user.append(game)
            time.sleep(1)

        return games_by_user

    def fetch_games(self):
        log.debug(self.config)

        new_games = []
        perftype_counter = collections.Counter()
        opening_counter = collections.Counter()

        games_by_user = self._fetch_games_by_user()

        if games_by_user:
            for game_json, game_pgn in [
                (
                    game,
                    games_client.export(
                        game["id"],
                        literate="true",
                        as_pgn=True,
                        opening="true",
                        tags="true",
                        moves="true",
                        evals="true",
                    ),
                )
                for game in games_by_user
            ]:
                game = self.pgn_to_game(game_pgn)
                chessli_game = Game(
                    pgn=game, json=game_json, config=self.config, paths=self.paths
                )

                if self.config.store:
                    log.debug(f"Storing {in_bold(chessli_game.name)}...")
                    chessli_game.store()

                new_games.append(chessli_game)

                perftype_counter.update([game_json["perf"]])
                opening_counter.update([game.headers["Opening"]])

            if self.config.verbosity >= 1:
                self._print_games_table(perftype_counter)
                self._print_openings_table(opening_counter)

            self._store_user_config()

        else:
            console.log(
                f"No new games to fetch since {in_bold(self.config.since_enum)}. Time to play! :fire:"
            )
            new_games = []
        return new_games

    @staticmethod
    def pgn_to_game(pgn: str) -> Optional[chess.pgn.Game]:
        return chess.pgn.read_game(io.StringIO(pgn))

    @staticmethod
    def counter_to_table(counter: collections.Counter, title: str, columns: List[str]):
        table = Table(*columns, title=f"{in_bold(title)}]")
        for game, count in counter.items():
            table.add_row(game, str(count))
        return table


@dataclass
class GamesReader:
    paths: ChessliPaths
    config: DictConfig

    def __post_init__(self):
        self._games = self.read_games()

    @property
    def path(self):
        return self.paths.games_dir

    @property
    def game_files(self) -> List[Path]:
        if self.config.perf_type is not None:
            game_path = self.path / self.config.perf_type
        else:
            game_path = self.path
        return list(game_path.glob("**/*.pgn"))

    @property
    def games(self) -> List[Any]:
        return self._games

    def read_games(self):
        games = [
            Game(
                pgn=chess.pgn.read_game(io.StringIO(pgn.read_text())),
                json=OmegaConf.load(pgn.with_suffix(".json")),
                config=self.config,
                paths=self.paths,
            )
            for pgn in self.game_files
        ]
        return games

    def ls(self) -> None:
        for game in self.games:
            print(game)

    @property
    def last_game(self) -> "Game":
        return self._games[-1]


@dataclass
class Game(MistakeFinderMixin, OpeningExtractorMixin, object):
    config: Optional[DictConfig] = None
    paths: Optional[ChessliPaths] = None
    pgn: Optional[chess.pgn.Game] = None
    json: Optional[Union[Dict, DictConfig]] = None

    def __str__(self) -> str:
        return f" - {self.name}"

    @property
    def name(self):
        return f"{self.pgn.headers['White']}_vs_{self.pgn.headers['Black']}_{self.json['id']}"

    @property
    def path(self) -> Path:
        path = self.paths.games_dir / self.json["perf"]
        path.mkdir(exist_ok=True)
        return path

    def store(self, as_pgn: bool = True, as_json: bool = True) -> None:
        if as_pgn:
            (self.path / self.name).with_suffix(".pgn").write_text(
                str(self.pgn), encoding="utf_8"
            )
        if as_json:
            for key, value in self.json.items():
                if isinstance(value, datetime):
                    self.json[key] = str(value)
            OmegaConf.save(
                config=OmegaConf.create(self.json),
                f=(self.path / self.name).with_suffix(".json"),
            )


@dataclass
class GamesCollection:
    games: List[Game]
    config: Optional[DictConfig]
    paths: Optional[ChessliPaths]
    mistakes: List[Mistake] = field(init=False)

    def __post_init__(self) -> None:
        self.mistakes = [mistakes for game in self.games for mistakes in game.mistakes]

    def get_df(self):
        return pd.DataFrame(data=[mistake.items for mistake in self.mistakes])

    def export_csv(self) -> None:
        time_stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        games_export_path = (
            self.paths.mistakes_dir / f"games_mistakes_export_{time_stamp}.csv"
        )
        self.get_df().to_csv(path_or_buf=games_export_path, index=False)
        log.info(f"Exported games mistakes as `csv` at {in_bold(games_export_path)}")

    def ankify_games(self) -> None:
        for game in track(self.games, description="Ankifying your mistakes...\n"):
            num_mistakes = len(game.mistakes)
            log.info(
                f"Found {in_bold(num_mistakes, 'red')} mistakes in the game {in_bold(game.name)}."
            )
            if num_mistakes == 0:
                continue
            mistake_file_path = (self.paths.mistakes_dir / game.name).with_suffix(".md")

            apy_header = "model: Chessli Games\ntags: chess::game_analysis\ndeck: Chessli::games\nmarkdown: False\n\n"

            md_notes = [mistake.md for mistake in game.mistakes]
            md = f"{apy_header}"
            for md_note in md_notes:
                md += f"{md_note}\n\n"
            mistake_file_path.write_text(md)

            import_to_anki_via_apy(file_path=mistake_file_path)
