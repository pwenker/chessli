from datetime import datetime

import typer
from omegaconf import DictConfig
from rich import print

from chessli import __version__
from chessli.enums import SinceEnum
from chessli.utils import as_title, convert_since_enum_to_millis


def _get_config_from_ctx(ctx: typer.Context) -> DictConfig:
    chessli_paths = ctx.parent.params["paths"]
    active_cmd_name = ctx.parent.command.name
    if active_cmd_name == "games":
        return chessli_paths.user_games_config
    elif active_cmd_name == "openings":
        return chessli_paths.user_openings_config
    else:
        raise NotImplementedError(
            f"There is no config for the cmd name {active_cmd_name}"
        )


def since_callback(ctx: typer.Context, value: SinceEnum):
    if value == SinceEnum.last_time:
        config = _get_config_from_ctx(ctx)
        if config.last_fetch_time is None:
            config.last_fetch_time = str(datetime.now())
            # ctx.parent.params["paths"] = chessli_paths
    return value.value


def version_callback(value: bool):
    if value:
        print(as_title(f"Chessli {__version__}"))
        raise typer.Exit()
