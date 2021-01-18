from enum import Enum
from pathlib import Path

import berserk

import chessli

project_path = Path(chessli.__file__).parent.parent
configs_path = project_path / "configs"

try:
    with (configs_path / "lichess.token").open("r") as f:
        token = f.read()
except FileNotFoundError:
    token = ""

try:
    with (configs_path / "lichess.user").open("r") as f:
        default_user = f.read()
except FileNotFoundError:
    default_user = None

session = berserk.TokenSession(token.strip())
berserk_client = berserk.Client(session=session)


def generate_path_container(user_name: str):
    class ChessliPath(Enum):
        project_path = Path(chessli.__file__).parent.parent
        configs = project_path / "configs"
        puzzles = project_path / "data" / "puzzles"
        user_path = project_path / "data" / user_name
        games = user_path / "games"
        mistakes = user_path / "mistakes"
        openings = user_path / "openings"

        @property
        def fetching(self):
            return (self.configs.value / "fetching").with_suffix(".yml")

    return ChessliPath
