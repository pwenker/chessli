from pathlib import Path

import berserk
from appdirs import user_config_dir, user_data_dir
from omegaconf import OmegaConf


class ChessliPath:
    @property
    def data_dir(self):
        data_dir = Path(user_data_dir("chessli"))
        data_dir.mkdir(exist_ok=True)
        return data_dir

    @property
    def configs_dir(self):
        configs_dir = Path(user_config_dir("chessli"))
        configs_dir.mkdir(exist_ok=True)
        return configs_dir

    @property
    def main_config(self):
        main_config_path = self.configs_dir / "config.yml"
        main_config_path.touch(exist_ok=True)
        user_config = OmegaConf.load(main_config_path)
        return user_config


class ChessliUserPaths(ChessliPath, object):
    def __init__(self, user_name: str):
        self.user_name = user_name

    @property
    def user_data_dir(self):
        user_data_dir = self.data_dir / self.user_name
        user_data_dir.mkdir(exist_ok=True)
        return user_data_dir

    @property
    def user_configs_dir(self):
        user_configs_dir = self.configs_dir / self.user_name
        user_configs_dir.mkdir(exist_ok=True)
        return user_configs_dir

    @property
    def games_folder(self):
        games_folder = self.user_data_dir / "games"
        games_folder.mkdir(exist_ok=True)
        return games_folder

    @property
    def openings_folder(self):
        openings_folder = self.user_data_dir / "openings"
        openings_folder.mkdir(exist_ok=True)
        return openings_folder

    @property
    def mistakes_folder(self):
        mistakes_folder = self.user_data_dir / "mistakes"
        mistakes_folder.mkdir(exist_ok=True)
        return mistakes_folder

    @property
    def tactics_folder(self):
        tactics_folder = self.user_data_dir / "tactics"
        tactics_folder.mkdir(exist_ok=True)
        return tactics_folder

    @property
    def user_config(self):
        user_config_path = self.user_configs_dir / "config.yml"
        user_config_path.touch(exist_ok=True)
        user_config = OmegaConf.load(user_config_path)
        return user_config

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


main_config = ChessliPath().main_config
session = berserk.TokenSession(main_config.token)
berserk_client = berserk.Client(session=session)
