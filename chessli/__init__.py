"""
A free and open source chess improvement app that combines the power of Lichess and Anki.
"""
__version__ = "0.2.2"


from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

import appdirs
import berserk
from omegaconf import DictConfig, OmegaConf
from rich.console import Console

from chessli.rich_logging import log

console = Console()

__all__ = ["ChessliPaths", "main_config", "berserk_client", "users_client"]


def get_berserk_client(token):
    if token is not None:
        session = berserk.TokenSession(token)
        return berserk.Client(session=session)
    else:
        return berserk.Client()


class AnkifyError(RuntimeError):
    """
    Could not ankify. Have you set up `apy` correctly?
    """


@dataclass
class PathCreatorMixin:
    @staticmethod
    def _maybe_make_dirs(dirs: List[Path]) -> None:
        for dir in dirs:
            dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _maybe_touch_files(files: List[Path]) -> None:
        for file in files:
            file.touch(exist_ok=True)


@dataclass
class ChessliPaths(PathCreatorMixin, object):
    user_name: str
    data_dir: Path = Path(appdirs.user_data_dir("chessli"))
    configs_dir: Path = Path(appdirs.user_config_dir("chessli"))
    main_config_path: Path = field(init=False)
    user_data_dir: Path = field(init=False)
    user_configs_dir: Path = field(init=False)
    user_config_path: Path = field(init=False)
    games_dir: Path = field(init=False)
    openings_dir: Path = field(init=False)
    mistakes_dir: Path = field(init=False)
    tactics_dir: Path = field(init=False)

    def __post_init__(self) -> None:
        # Main paths
        self._maybe_make_dirs([self.data_dir, self.configs_dir])
        self.main_config_path = self.configs_dir / "config.yml"
        self._maybe_touch_files([self.main_config_path])

        # User-specific paths
        self.user_data_dir = self.data_dir / self.user_name
        self.user_configs_dir = self.configs_dir / self.user_name
        self.games_dir = self.user_data_dir / "games"
        self.openings_dir = self.user_data_dir / "openings"
        self.mistakes_dir = self.user_data_dir / "mistakes"
        self.tactics_dir = self.user_data_dir / "tactics"

        self._maybe_make_dirs(
            [
                self.user_data_dir,
                self.user_configs_dir,
                self.games_dir,
                self.openings_dir,
                self.mistakes_dir,
                self.tactics_dir,
            ]
        )
        self.user_config_path = self.user_configs_dir / "config.yml"
        self._maybe_touch_files([self.user_config_path])

        self._user_config = OmegaConf.load(self.user_config_path)
        self._main_config = OmegaConf.load(self.main_config_path)

    @property
    def main_config(self):
        return self._main_config

    @property
    def user_config(self):
        return self._user_config

    @user_config.setter
    def set_user_config(self, config):
        self._user_config = config

    @main_config.setter
    def set_main_config(self, config):
        self._main_config = config

    def __str__(self) -> str:
        return f"""
        Configs Directory: {self.configs_dir}
        Data Directory: {self.data_dir}
        General Config: {self.main_config_path}

        User Name: {self.user_name}
        User Configs Directory: {self.user_configs_dir}
        User Config Path: {self.user_config_path}
        User data directory: {self.user_data_dir}
        """


main_config = ChessliPaths("dummy").main_config
berserk_client = get_berserk_client(main_config.token)
users_client = berserk_client.users
