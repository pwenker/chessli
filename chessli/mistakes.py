from dataclasses import dataclass
from typing import Any, Dict

from rich import print
from rich.console import Console
from rich.markdown import Markdown

from chessli.enums import Nag

console = Console()


def get_nag_name(nag: int) -> str:
    return {nag.value: nag.name for nag in Nag}[nag]


@dataclass
class Mistake:
    fen: str  # The fen of the board serves as ID
    comment: str
    ply: int
    move_color: str
    nag: Nag
    nag_name: str
    my_move: str
    best_move: str
    variation: str
    game: Any

    @property
    def game_items(self) -> Dict:
        return {k: v for k, v in self.game.headers.items()}

    @property
    def items(self) -> Dict:
        raw_items = {**vars(self), **self.game_items}
        dont_include = [
            "WhiteElo",
            "WhiteTitle",
            "WhiteRatingDiff",
            "UTCDate",
            "game",
            "BlackTitle",
            "BlackRatingDiff",
            "BlackElo",
            "UTCTime",
        ]
        items = {k: v for k, v in raw_items.items() if k not in dont_include}
        if items["move_color"] == "White":
            items["Me"] = raw_items["White"]
            items["Opponent"] = raw_items["Black"]
            items["My Elo"] = raw_items["WhiteElo"]
            items["Opponent Elo"] = raw_items["BlackElo"]
        elif items["move_color"] == "Black":
            items["Me"] = raw_items["Black"]
            items["Opponent"] = raw_items["White"]
            items["My Elo"] = raw_items["BlackElo"]
            items["Opponent Elo"] = raw_items["WhiteElo"]

        return items

    @property
    def md(self) -> str:
        md = "# Mistake\n"
        for key, value in self.items.items():
            if key == "game":
                continue
            md += f"## {key.replace('_', ' ').title()}\n"
            md += f"{value}\n"
        return md

    @property
    def pprint(self):
        console.print(Markdown(self.md))
