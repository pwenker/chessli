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

test_requirements = [
    "pytest>=6.0",
    "pytest-cov",
    "pytest-sugar",
]

setup(
    name="chessli",
    url="https://github.com/pwenker/chessli",
    version="0.1",
    entry_points={
        "console_scripts": [
            "chessli=chessli.cli.main:app",
        ],
    },
    author="Pascal Wenker",
    author_email="pwenker@posteo.de",
    install_requires=requirements,
    tests_require=test_requirements,
    packages=find_packages(),
)
