![Thumbnail](https://github.com/pwenker/chessli/blob/main/imgs/chessli.png?raw=true)

_A free and open-source chess improvement app that combines the power of Lichess and Anki._

|  | Chessli |
| --- | --- |
| Project                | [![GitHub Repo stars](https://img.shields.io/github/stars/pwenker/chessli?style=social)](https://github.com/pwenker/chessli) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/pwenker/chessli) ![Lines of code](https://img.shields.io/tokei/lines/github/pwenker/chessli)
| Activity & Issue Tracking | ![GitHub last commit](https://img.shields.io/github/last-commit/pwenker/chessli) [![GitHub issues](https://img.shields.io/github/issues-raw/pwenker/chessli)](https://github.com/pwenker/chessli/issues?q=is%3Aopen+is%3Aissue) [![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/pwenker/chessli)](https://github.com/pwenker/chessli/issues?q=is%3Aissue+is%3Aclosed)  |
| PyPI                      | [![PyPI](https://img.shields.io/pypi/v/chessli)](https://pypi.org/project/chessli/)                                                                                                                                  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chessli) [![Downloads](https://pepy.tech/badge/chessli/month)](https://pepy.tech/project/chessli)|
| Build & Health                  | ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/pwenker/chessli/CI) ![Codecov](https://img.shields.io/codecov/c/github/pwenker/chessli) |
| Docs | [![Documentation Status](https://img.shields.io/badge/Docs-live-green)](https://pwenker.com/chessli) [![Tutorial](https://img.shields.io/badge/Tutorial-active-brightgreen)](https://pwenker.com/chessli/tutorial/how_to_set_up_chessli) |
| News & Updates | [![Twitter Follow](https://img.shields.io/twitter/follow/PascalWenker?style=social)](https://twitter.com/PascalWenker) [![GitHub followers](https://img.shields.io/github/followers/pwenker?style=social)](https://github.com/pwenker)|

## Demos

### CLI Demo (watch whole video on [Youtube](https://www.youtube.com/embed/XbD71Kq7cx4))

![CLI DEMO GIF](https://github.com/pwenker/chessli/blob/main/imgs/chessli_cli_demo.gif?raw=true)

### Anki Cards Demo (watch whole video on [Youtube](https://www.youtube.com/watch?v=Diew--CWlsI))

![CLI CARDS GIF](https://github.com/pwenker/chessli/blob/main/imgs/chessli_cards_demo.gif?raw=true)

## Documentation
Check out the [documentation](https://pwenker.com/chessli):

|  | Tutorial |
| --- | --- |
Setup chessli | [How to set chessli up](https://pwenker.com/chessli/tutorial/how_to_set_up_chessli)
Games & Mistakes | [How to learn from your games](https://pwenker.com/chessli/tutorial/how_to_learn_from_your_games)
Openings | [How to build an opening repertoire](https://pwenker.com/chessli/tutorial/how_to_create_an_opening_repertoire)
Tactics | [How to get better at tactics](https://pwenker.com/chessli/tutorial/how_to_get_better_at_tactics)
Anki Cards | [How to use chessli's anki cards](https://pwenker.com/chessli/tutorial/how_to_use_chesslis_anki_cards)


## Features

- **Automatically fetch your games** and played tactics puzzles from [`lichess`](https://www.lichess.org) via the [`berserk`](https://github.com/rhgrant10/berserk) python client for the Lichess API.!
- **Find your mistakes** by parsing your games and analysing them with [`python-chess`](https://github.com/niklasf/python-chess).
- **Build a simple opening repertoire and list your known openings**
- **Spaced repetition & Retrieval Practice**: Automatically (via [`apy`](https://github.com/lervag/apy)) or manually (via csv export) add your game mistakes, your openings and your tackled lichess puzzles into [`Anki`](https://apps.ankiweb.net/)
- **Stats and visualizations**: Seamlessly show `lichess leaderboards` or plot your `rating history`.


## Getting Started

### Installation
1. Install `pip`. See [here](https://pip.pypa.io/en/stable/installing/) for help.

2.  Install chessli with `pip`:
```console
pip install chessli
```
That's it!

## Basic Usage
To get help about `chessli`s commands, open your console and type:
```console
chessli --help
```
The same works for subcommands, e.g., :
```console
chessli games --help
```
You can find an overview of all availabe cli-commands [here](https://pwenker.com/chessli/cli/) in
the docs.

### Tutorial
Now as you are familiar with the basics, you might want to walk through the tutorial to get the most
out of `chessli`!
Start with [setting up chessli](https://pwenker.com/tutorial/how_to_set_up_chesslid).

## Acknowledgments

|  | Acknowledgements |
| --- | --- |
| [`Lichess`](https://lichess.org) | A free, no-ads, open source chess server that let's everyone play chess! Think about whether to [become a patron](https://lichess.org/patron)! :) |
| [`Anki`](https://apps.ankiweb.net/) | A free and open-source flashcard program using spaced-repetition, a technique from cognitive science for fast and long-lasting memorization.  I couldn't imagine learning without it anymore. |
| [`Anki Card Templates`](https://ankiweb.net/shared/info/1082754005) | The interactive chess functionality on Chessli's anki cards is based from [these fantastic cards](https://ankiweb.net/shared/info/1082754005).|
| [`python-chess`](https://github.com/niklasf/python-chess) | Most of the heavy lifting, e.g. parsing games, finding mistakes, extracting openings, etc. is done with `python-chess`. |
| [`berserk`](https://github.com/rhgrant10/berserk) |  The communication between `lichess` and `chessli` is performed via `berserk` |
| [`typer`](https://github.com/tiangolo/typer) | The `chessli` `cli` is built with the great `typer` |
| [`rich`](https://github.com/willmcgugan/rich) | The rich colors and fancy tables are made possible by `rich` |
| [`apy`](https://github.com/lervag/apy/) | Importing cards directly into anki without csv-export can be done via `apy` |
