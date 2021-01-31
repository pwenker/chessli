import subprocess
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

import berserk
import pandas as pd
import typer
from omegaconf import DictConfig, OmegaConf
from rich import print
from rich.console import Console
from rich.table import Table

from chessli import AnkifyError, ChessliPaths
from chessli.enums import SinceEnum

console = Console()


def create_config_from_options(context_params: Dict) -> DictConfig:
    def _strip_non_compatible_elements(context_params: Dict) -> Dict:
        return {
            k: v for k, v in context_params.items() if not isinstance(v, ChessliPaths)
        }

    config = OmegaConf.create(_strip_non_compatible_elements(context_params))
    return config


def extract_context_info(ctx: typer.Context) -> Tuple["ChessliPaths", "DictConfig"]:
    chessli_paths = ctx.parent.params["paths"]
    cli_params = {**ctx.parent.params, **ctx.params}
    try:
        cli_params["perf_type"] = (
            None if not cli_params["perf_type"] else cli_params["perf_type"]
        )
    except KeyError:
        pass
    cli_config = create_config_from_options(cli_params)
    return chessli_paths, cli_config


def convert_since_enum_to_millis(since_enum: SinceEnum, config: DictConfig):
    if since_enum == SinceEnum.one_hour:
        since = datetime.now() - timedelta(hours=1)
    elif since_enum == SinceEnum.yesterday:
        since = datetime.now() - timedelta(days=1)
    elif since_enum == SinceEnum.last_week:
        since = datetime.now() - timedelta(days=7)
    elif since_enum == SinceEnum.last_month:
        since = datetime.now() - timedelta(days=31)
    elif since_enum == SinceEnum.last_year:
        since = datetime.now() - timedelta(days=365)
    elif since_enum == SinceEnum.forever:
        since = datetime.now() - timedelta(days=365 * 42)  # roughly forever
    elif since_enum == SinceEnum.last_time:
        since = datetime.fromisoformat(config.last_fetch_time)
    return berserk.utils.to_millis(since)


def import_to_anki_via_apy(file_path: Path) -> None:
    try:
        subprocess.run(
            ["apy", "add-from-file", file_path], shell=True, check=True, input=b"n"
        )
    except subprocess.CalledProcessError as e:
        raise AnkifyError(e)


####################################################################################################
#                          Some custom functions to make strings prettier                          #
####################################################################################################


def in_bold(string: Union[str, int, Path], color: str = "blue") -> str:
    return f"[bold][{color}]{string}[/{color}][/bold]"


def as_title(string: str) -> str:
    return f":fire: {in_bold(string.upper())} :fire:"
