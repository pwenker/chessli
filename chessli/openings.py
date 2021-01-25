import subprocess
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

from rich import print
from rich.console import Console
from rich.markdown import Markdown

console = Console()


@dataclass
class Opening:
    name: str
    site: str
    eco: str
    moves: str
    config: Any

    def __str__(self):
        return f"{self.eco} - {self.name}"

    @property
    def items(self) -> Dict:
        return vars(self)

    @property
    def md(self) -> str:
        md = "# Opening\n"
        for key, value in self.items.items():
            if key != "config":
                md += f"## {key.replace('_', ' ').title()}\n"
                md += f"{value}\n"
        return md

    @property
    def pprint(self) -> None:
        console.print(Markdown(self.md))

    @property
    def path(self) -> Path:
        path = self.config.paths.openings.value
        path.mkdir(parents=True, exist_ok=True)
        return (path / str(self)).with_suffix(".md")

    def exists(self) -> bool:
        return self.path.exists()

    @property
    def apy_header(self) -> str:
        return "model: Chessli Openings\ntags: chess::openings\ndeck: Chessli::openings\nmarkdown: False\n\n"

    def store(self) -> None:
        if not self.exists():
            console.log(f"Storing: {str(self)}")
            md = f"{self.apy_header}"
            md += f"{self.md}\n\n"
            self.path.write_text(md)
        else:
            console.log(f"{str(self)} already learned :)")

    def ankify(self):
        if self.exists():
            subprocess.run(["apy", "add-from-file", self.path], input=b"n")
        else:
            console.log(
                "To ankify, you first need to store the opening with `opening.store()`"
            )


class ECOVolume(str, Enum):
    A = "Volume A: Flank openings"
    B = "Volume B: Semi-Open Games other than the French Defense"
    C = "Volume C: Open Games and the French Defense"
    D = "Volume D: Closed Games and Semi-Closed Games"
    E = "Volume E: Indian Defenses"


def list_known_openings(eco_volume: Optional[ECOVolume], config):
    opening_dict = defaultdict(list)
    known_openings = sorted([f.stem for f in config.paths.openings.value.glob("*.md")])
    print(
        f":fire: You already know a total of [bold magenta]{len(known_openings)}[/bold magenta] openings!!! :fire:",
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
