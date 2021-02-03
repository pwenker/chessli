from datetime import datetime

import typer
from rich import print

from chessli import __version__
from chessli.enums import SinceEnum
from chessli.utils import as_title, convert_since_enum_to_millis


def version_callback(value: bool):
    if value:
        print(as_title(f"Chessli {__version__}"))
        raise typer.Exit()


def since_callback(ctx: typer.Context, value: SinceEnum):
    if value == SinceEnum.last_time:
        chessli_paths = ctx.parent.params["paths"]
        if chessli_paths.user_config.last_fetch_time is None:
            chessli_paths.user_config.last_fetch_time = str(datetime.now())
            ctx.parent.params["paths"] = chessli_paths
    return value.value
