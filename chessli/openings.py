from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, ItemsView, List, Optional, Set, Tuple, Union

import chess
import pandas as pd
from omegaconf import DictConfig
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from chessli import ChessliPaths
from chessli.rich_logging import log
from chessli.utils import import_to_anki_via_apy, in_bold

console = Console()


class ECOVolume(str, Enum):
    A = "Volume A: Flank openings"
    B = "Volume B: Semi-Open Games other than the French Defense"
    C = "Volume C: Open Games and the French Defense"
    D = "Volume D: Closed Games and Semi-Closed Games"
    E = "Volume E: Indian Defenses"


class ECOVolumeLetter(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


@dataclass
class Opening:
    name: str
    site: str
    eco: str
    moves: str
    config: Any
    paths: ChessliPaths

    def __str__(self):
        return f"{self.eco} - {self.name}"

    @property
    def items(self) -> Dict:
        return vars(self)

    @property
    def anki_items(self) -> Dict:
        anki_items = {
            k: v for k, v in vars(self).items() if k not in ["config", "paths"]
        }
        return anki_items

    @property
    def md(self) -> str:
        md = "# Opening\n"
        for key, value in self.anki_items.items():
            md += f"## {key.replace('_', ' ').title()}\n"
            md += f"{value}\n"
        return md

    @property
    def pprint(self) -> None:
        console.print(Markdown(self.md))

    @property
    def path(self) -> Path:
        openings_dir = self.paths.openings_dir
        return (openings_dir / str(self)).with_suffix(".md")

    def exists(self) -> bool:
        return self.path.exists()

    @property
    def apy_header(self) -> str:
        return "model: Chessli Openings\ntags: chess::openings\ndeck: Chessli::openings\nmarkdown: False\n\n"

    def store(self, force: bool = False) -> None:
        if not self.exists() or force:
            log.info(f"Storing opening: {in_bold(str(self))}")
            md = f"{self.apy_header}"
            md += f"{self.md}\n\n"
            self.path.write_text(md)
        else:
            log.info(
                f"Ignoring {in_bold(str(self), 'yellow')}. You already know that opening :)"
            )

    def ankify(self):
        if self.exists():
            import_to_anki_via_apy(file_path=self.path)
        else:
            console.log(
                "To ankify, you first need to store the opening with `opening.store()`"
            )


@dataclass
class OpeningsCollection:
    config: Optional[DictConfig] = None
    paths: Optional[ChessliPaths] = None
    openings: Optional[List[Opening]] = None

    @classmethod
    def from_games(
        cls, config: DictConfig, paths: ChessliPaths, games: List["Game"]
    ) -> "OpeningsCollection":
        return cls(config, paths, [game.opening for game in games])

    def get_df(self):
        return pd.DataFrame(data=[opening.anki_items for opening in self.openings])

    def empty(self) -> bool:
        return not bool(len(self.openings))

    def export_csv(self) -> None:
        if self.empty():
            return
        time_stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        openings_export_path = (
            self.paths.openings_dir / f"openings_export_{time_stamp}.csv"
        )
        self.get_df().to_csv(path_or_buf=openings_export_path, index=False)
        log.info(f"Exported openings as csv at {openings_export_path}")

        self.store_openings()

    def store_openings(self) -> None:
        if self.empty():
            return None
        for opening in self.openings:
            opening.store()
        log.info(f"Stored openings at {self.paths.openings_dir}")

    def ankify_openings(self) -> None:
        if self.empty():
            return None
        for opening in self.openings:
            opening.store()
            log.info(f"Ankifying opening: {in_bold(opening.name)}")
            opening.ankify()


def list_known_openings(
    eco_volume: Optional[ECOVolumeLetter], chessli_paths: ChessliPaths
) -> None:
    opening_dict = defaultdict(list)
    known_openings = sorted([f.stem for f in chessli_paths.openings_dir.glob("*.md")])
    print(
        f":fire: You already know a total of {in_bold(len(known_openings))} openings!!! :fire:",
        end="\n\n",
    )

    for opening in known_openings:
        opening_dict[opening[0]].append(opening)

    for key, value in opening_dict.items():
        if eco_volume is None or key == eco_volume:
            eco_volume_title = f"{ECOVolume[key]} ({len(value)})"
            print(f"[bold blue]{eco_volume_title}[/bold blue]!", end="\n\n")
            for val in value:
                print("✔️ ", val)
            print("")


def print_openings(openings: List["Opening"]):
    table = Table("", "Name", "ECO", title="New Openings")

    for opening in openings:
        if opening.exists():

            new_str = ""
            name_str = f"[grey]{opening.name}[/grey]"
            eco_str = f"[grey]{opening.eco}[/grey]"
        else:
            new_str = ":new:"
            name_str = f"[green]{opening.name}[/green]"
            eco_str = f"[green]{opening.eco}[/green]"

        table.add_row(new_str, eco_str, name_str)

    console.print(table)


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
