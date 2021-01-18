from setuptools import find_packages, setup

requirements = []


requirements = [
    "chess",
    "typer",
    "rich",
    "omegaconf",
    "berserk",
    "pandas",
    "matplotlib",
    "seaborn",
]

setup(
    name="chessli",
    version="0.1",
    entry_points={
        "console_scripts": [
            "chessli=chessli.cli.main:app",
        ],
    },
    author="Pascal Wenker",
    install_requires=requirements,
    packages=find_packages(),
)
