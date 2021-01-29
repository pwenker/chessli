import collections
import datetime
import io
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import chess.pgn
import chess.svg
from omegaconf import DictConfig, OmegaConf
from rich import print
from rich.console import Console
from rich.progress import track
from rich.table import Table

from chessli import ChessliPaths, berserk_client
from chessli.enums import Color
from chessli.mistakes import Mistake, get_nag_name
from chessli.openings import Opening
from chessli.rich_logging import log
from chessli.utils import in_bold

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
        self.config.fetch_time = str(datetime.datetime.now())
        new_fetch_config = OmegaConf.create(
            {
                "since_millis": self.config.since_millis,
                "last_fetch_time": self.config.fetch_time,
            }
        )
        OmegaConf.save(config=new_fetch_config, f=self.paths.user_config_path)

    def _fetch_games_by_user(self) -> List:
        console.log(f"Fetching games of {in_bold(self.config.user)}.")
        games_by_user = [
            game
            for game in games_client.export_by_player(
                max=self.config.max,
                username=self.config.user,
                since=int(self.config.since_millis),
                perf_type=self.config.perf_type,
            )
        ]
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
                    log.debug(f"Storing {chessli_game.name}...")
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
class OpeningExtractorMixin:
    pgn: Optional[chess.pgn.Game] = None
    config: Optional[DictConfig] = None
    paths: Optional[ChessliPaths] = None

    @property
    def opening(self):
        game = self.pgn
        info = game.headers

        def get_moves(game) -> str:
            moves = []
            board = game.board()
            game = game.next()
            while info["Opening"] not in game.comment:
                move = game.move
                moves.append(move)
                game = game.next()
            move = game.move
            moves.append(move)
            move_list = board.variation_san(moves)
            return move_list

        return Opening(
            name=info["Opening"],
            eco=info["ECO"],
            site=info["Site"],
            moves=get_moves(game),
            config=self.config,
            paths=self.paths,
        )


@dataclass
class MistakeFinderMixin:
    pgn: Optional[chess.pgn.Game] = None
    config: Optional[DictConfig] = None

    @property
    def player(self,) -> Color:
        return (
            Color.white
            if self.pgn.headers["White"] == self.config.user
            else Color.black
        )

    def my_move(self, move_color: Color) -> bool:
        return True if self.player.value == move_color else False

    @property
    def mistakes(self,) -> List["Mistake"]:
        _mistakes = []

        game = self.pgn

        while game is not None:
            whose_turn = not game.turn()
            move_color = "White" if whose_turn else "Black"
            if self.my_move(whose_turn):
                if game.nags:
                    parent = game.parent
                    parent_board = parent.board()
                    if len(parent.variations) > 1:
                        assert len(parent.variations) == 2
                        variation_moves = str(parent.variations[1])
                    nag = list(game.nags)[0]
                    nag_name = get_nag_name(nag)

                    _mistakes.append(
                        Mistake(
                            fen=parent_board.fen(),
                            comment=game.comment,
                            ply=parent.ply(),
                            move_color=move_color,
                            nag=nag,
                            nag_name=nag_name,
                            my_move=game.san(),
                            best_move=parent.variations[1].san(),
                            variation=variation_moves,
                            game=self.pgn,
                        )
                    )
            game = game.next()

        return _mistakes


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
                if isinstance(value, datetime.datetime):
                    self.json[key] = str(value)
            OmegaConf.save(
                config=OmegaConf.create(self.json),
                f=(self.path / self.name).with_suffix(".json"),
            )
