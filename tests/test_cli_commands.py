from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

import pytest
from typer.testing import CliRunner

from chessli.cli.main import app

runner = CliRunner()


main_commands = [
    "--help",
    "--version",
    "-v",
    "-vv",
    "-vvv",
    "--user DrNykterstein",
    "--show-configs",
    "--show-paths",
]
games_commands = [
    "games --help",
    "games ls --help",
    "games ls --perf-type classical",
    "games fetch --help",
    "games fetch",
    "games fetch --since last-year --perf-type classical --perf-type bullet --perf-type blitz --max 10 --store",
    "games ankify",
    "games ankify --help",
    "games ankify --since last-week --perf-type rapid --max 15 --export-only",
    "games ankify --since one-hour --perf-type classical --max 0 --directly",
]
tactics_commands = [
    "tactics --help",
    "tactics ls --help",
    "tactics ls --new",
    "tactics ls --old",
    "tactics ankify --help",
    "tactics ankify --new --export-only",
    "tactics ankify --new --failed-only",
    "tactics ankify --won-only",
    "tactics ankify --new --directly",
]

openings_commands = [
    "openings --help",
    "openings ls --help",
    "openings ls --eco A",
    "openings ls --perf-type blitz",
    "openings ankify --help",
    "openings ankify",
    "openings ankify --new-openings-only --since last-time --max 1 --perf-type blitz --perf-type classical --export-only",
]
stats_commands = [
    "stats --help",
    "stats leaderboard --help",
    "stats leaderboard --type classical",
    # "stats rating --help",
    # "stats rating --type classical",
]


def _basic(command):
    command = f"--user DrNykterstein {command}"
    result = runner.invoke(app, command.split())
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "command", main_commands,
)
def test_chessli_commands(command):
    _basic(command)


@pytest.mark.parametrize(
    "command", games_commands,
)
def test_chessli_games_commands(command):
    _basic(command)


@pytest.mark.requires_api_token
@pytest.mark.parametrize(
    "command", tactics_commands,
)
def test_chessli_tactics_commands(command):
    _basic(command)


@pytest.mark.parametrize(
    "command", openings_commands,
)
def test_chessli_openings_commands(command):
    _basic(command)


@pytest.mark.parametrize(
    "command", stats_commands,
)
def test_chessli_stats_commands(command):
    _basic(command)


def create_cli_demo_script():
    DEMO = ""

    class TestCommandsGroup(Enum):
        main = main_commands
        games = games_commands
        openings = openings_commands
        tactics = tactics_commands

    def slowly_typed(cmd: str) -> str:
        return f"xdotool type --delay 100 '>>> {cmd}'\n"

    def cmd_as_string(cmd: List) -> str:
        sub_cmd = " ".join(cmd)
        return f"chessli {sub_cmd}"

    def create_line_break() -> str:
        lbr = r"printf '\n\n'"
        return f"{lbr}\n"

    def clear_screen() -> str:
        return "xdotool exec 'clear'\n"

    def create_sleep(secs: int = 1) -> str:
        return f"sleep {secs}\n"

    for cmd_grp in TestCommandsGroup:
        DEMO += "\n\n"
        DEMO += f"toilet --metal {cmd_grp.name.upper()}"
        DEMO += "\n\n"
        for cmd in cmd_grp.value:
            cmd_str = cmd_as_string(cmd)
            create_sleep(1)
            DEMO += slowly_typed(cmd_str)
            create_sleep(1)
            DEMO += create_line_break()
            create_sleep(1)
            DEMO += f"{cmd_str}\n"
            create_sleep(2)
        DEMO += clear_screen()

    print(DEMO)

    demo_path = Path(".") / "run_demo.sh"
    demo_path.write_text(DEMO)


if __name__ == "__main__":
    create_cli_demo_script()
