import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

import berserk
from omegaconf import DictConfig, OmegaConf
from rich import print
from rich.console import Console
from rich.table import Table

from chessli.enums import SinceEnum

console = Console()


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


def df_to_apy(df):
    md = ""
    header = "model: Chessli Tactics\ntags: chess::tactics\ndeck: Chessli::tactics\nmarkdown: False\n\n"
    md += header
    for idx, row in df.iterrows():
        md += "# Note\n"
        for key, value in row.items():
            md += f"## {key}\n"
            md += f"{value}\n"
    return md


def create_config_from_options(context_params: Dict) -> DictConfig:
    config = OmegaConf.create(context_params)
    return config


def convert_since_enum_to_millis(since_enum, last_fetch_config):
    if since_enum == SinceEnum.one_hour:
        since = datetime.now() - timedelta(hours=1)
    elif since_enum == SinceEnum.yesterday:
        since = datetime.now() - timedelta(days=1)
    elif since_enum == SinceEnum.last_week:
        since = datetime.now() - timedelta(days=7)
    elif since_enum == SinceEnum.last_time:
        since = datetime.fromisoformat(last_fetch_config["fetch_time"])
    return berserk.utils.to_millis(since)


def ankify_with_apy(
    file_path: Path, apy_header: str, md_notes: List[str], ankify: bool = True
) -> None:
    # console.log(f"Ankify the game '{file_path.name}' with `apy`")
    md = f"{apy_header}"
    for md_note in md_notes:
        md += f"{md_note}\n\n"
    file_path.write_text(md)

    if ankify:
        subprocess.run(["apy", "add-from-file", file_path], input=b"n")
