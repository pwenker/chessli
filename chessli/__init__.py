from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

import berserk
from appdirs import user_config_dir, user_data_dir
from omegaconf import DictConfig, OmegaConf
from rich.console import Console

console = Console()


@dataclass
class PathCreaterMixin:
    @staticmethod
    def _maybe_make_dirs(dirs: List[Path]) -> None:
        for dir in dirs:
            dir.mkdir(exist_ok=True)

    @staticmethod
    def _maybe_touch_files(files: List[Path]) -> None:
        for file in files:
            file.touch(exist_ok=True)


@dataclass
class ChessliPaths(PathCreaterMixin, object):
    user_name: str
    data_dir: Path = Path(user_data_dir("chessli"))
    configs_dir: Path = Path(user_config_dir("chessli"))
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
        self.user_configs_dir = self.data_dir / self.user_name
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

    @property
    def main_config(self):
        return OmegaConf.load(self.main_config_path)

    @property
    def user_config(self):
        return OmegaConf.load(self.user_config_path)

    def __str__(self) -> str:
        return f"""
        Config directory: {self.configs_dir}
        Data directory: {self.data_dir}
        Main Config: {self.main_config}
        User name: {self.user_name}
        User configs directory: {self.user_configs_dir}
        User data directory: {self.user_data_dir}
        User Config: {self.user_config}
        """


main_config = ChessliPaths("dummy").main_config
token = main_config.token
if token is not None:
    console.log("Chessli found your token. Starting a TokenSession")
    session = berserk.TokenSession(token)
    berserk_client = berserk.Client(session=session)
else:
    console.log("Chessli did not found any token. Starting a normal Session")
    berserk_client = berserk.Client()
