import collections
import datetime
import io
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import chess.pgn
import chess.svg
from omegaconf import DictConfig, OmegaConf
from rich import print
from rich.console import Console
from rich.progress import track
from rich.table import Table

from chessli import berserk_client
from chessli.enums import Color
from chessli.mistakes import Mistake, get_nag_name
from chessli.openings import Opening

console = Console()


games_client = berserk_client.games


def pgn_to_game(pgn: str) -> Optional[chess.pgn.Game]:
    return chess.pgn.read_game(io.StringIO(pgn))


@dataclass
class GameManager:
    config: DictConfig

    def __post_init__(self):
        self._games = self.read_games()

    @property
    def path(self):
        path = self.config.paths.games.value
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def files(self) -> List[Path]:
        return list(self.path.glob("**/*.pgn"))

    @property
    def games(self) -> List[Any]:
        return self._games

    def read_games(self):
        games = [
            Game(
                pgn=chess.pgn.read_game(io.StringIO(pgn.read_text())),
                json=OmegaConf.load(pgn.with_suffix(".json")),
                config=self.config,
            )
            for pgn in self.files
        ]
        return games

    @property
    def last_game(self) -> "Game":
        return self._games[-1]

    def fetch_games(self):
        new_games = []
        perftype_counter = collections.Counter()
        opening_counter = collections.Counter()
        console.log(f"Fetching {self.config.user}'s games.")
        games_by_user = [
            game
            for game in games_client.export_by_player(
                max=20,
                username=self.config.user,
                since=int(self.config.since),
                perf_type=self.config.perf_type,
            )
        ]

        if games_by_user:
            for game_json, game_pgn in track(
                [
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
                ],
                description=f"Fetching additional game information...",
            ):
                game = pgn_to_game(game_pgn)
                chessli_game = Game(pgn=game, json=game_json, config=self.config)
                chessli_game.store()
                new_games.append(chessli_game)

                perftype_counter.update([game_json["perf"]])
                opening_counter.update([game.headers["Opening"]])

            table = Table("Game Type", "Number of Plays", title=f"New Games :fire:")
            for game, count in perftype_counter.items():
                table.add_row(game, str(count))
                # console.log(f":fire: Fetched {count} '{game}' game(s)")
            console.print(table)

            table = Table(
                "Opening Name", "Number of Plays", title=f"New Openings :fire:"
            )
            for opening, count in opening_counter.items():
                # console.log(f":fire: {count} '{opening}'")
                table.add_row(opening, str(count))
            console.print(table)

            self.config.fetch_time = str(datetime.datetime.now())
            new_fetch_config = OmegaConf.create(
                {"since": self.config.since, "fetch_time": self.config.fetch_time}
            )
            OmegaConf.save(
                config=new_fetch_config, f=self.config.paths.configs.fetching
            )
        else:
            console.log("You didn't play any game since, time to play! :fire: ♟️")
            new_games = []
        return new_games


@dataclass
class Game:
    config: DictConfig
    pgn: Optional[chess.pgn.Game]
    json: Optional[Union[Dict, DictConfig]]

    @property
    def name(self):
        return f"{self.pgn.headers['White']}_vs_{self.pgn.headers['Black']}_{self.json['id']}"

    @property
    def player(self) -> Color:
        return (
            Color.white
            if self.pgn.headers["White"] == self.config.user
            else Color.black
        )

    def my_move(self, move_color: Color) -> bool:
        return True if self.player.value == move_color else False

    @property
    def path(self):
        path = self.config.paths.games.value / self.json["perf"]
        path.mkdir(exist_ok=True, parents=True)
        return path

    def store(self, as_pgn: bool = True, as_json: bool = True):
        if as_pgn:
            (self.path / self.name).with_suffix(".pgn").write_text(str(self.pgn))
        if as_json:
            for key, value in self.json.items():
                if type(value) == datetime.datetime:
                    self.json[key] = str(value)
            OmegaConf.save(
                config=OmegaConf.create(self.json),
                f=(self.path / self.name).with_suffix(".json"),
            )

    def mistakes(self) -> Optional[List["Mistake"]]:
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
        )

    def apy_header(self):
        return "model: Chessli Games\ntags: chess::game_analysis\ndeck: Chessli::games\nmarkdown: False\n\n"
