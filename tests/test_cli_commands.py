from typer.testing import CliRunner
import pytest


from chessli.cli.main import app

runner = CliRunner()


@pytest.mark.parametrize(
    "command",
    [
        ("games", "ls"),
        ("openings", "ls"),
        ("tactics", "ls", "--old"),
        pytest.param(("tactics", "ls", "--new"), marks=pytest.mark.slow),
    ],
)
def test_chessli_commands(command):
    result = runner.invoke(app, command)
    assert result.exit_code == 0
