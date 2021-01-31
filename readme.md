![Thumbnail](https://github.com/pwenker/chessli/blob/main/imgs/chessli.png?raw=true)
_A free and open-source CHESS improvement program that combines the power
of Lichess and Anki._
|  | Description |
| --- | --- |
| Project                | ![GitHub Repo stars](https://img.shields.io/github/stars/pwenker/chessli?style=social) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/pwenker/chessli) ![Lines of code](https://img.shields.io/tokei/lines/github/pwenker/chessli)
| Activity & Issue Tracking | ![GitHub last commit](https://img.shields.io/github/last-commit/pwenker/chessli) ![GitHub issues](https://img.shields.io/github/issues-raw/pwenker/chessli) ![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/pwenker/chessli)  |
| PyPI                      | ![PyPI](https://img.shields.io/pypi/v/chessli)                                                                                                                                  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chessli) ![PyPI - Downloads](https://img.shields.io/pypi/dm/chessli) |
| Build & Health                  | ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/pwenker/chessli/CI) ![Codecov](https://img.shields.io/codecov/c/github/pwenker/chessli) |
| Docs | ![Documentation Status](https://img.shields.io/badge/Docs-live-green) ![](https://img.shields.io/badge/Tutorial-active-brightgreen) |

## Demos

### CLI Demo (watch whole video on [Youtube](https://www.youtube.com/embed/XbD71Kq7cx4))

![CLI DEMO GIF](https://github.com/pwenker/chessli/blob/main/imgs/chessli_cli_demo.gif?raw=true)

### Anki Cards Demo (watch whole video on [Youtube](https://www.youtube.com/embed/aj-FqJhPyyA))

![CLI CARDS GIF](https://github.com/pwenker/chessli/blob/main/imgs/chessli_cards_demo.gif?raw=true)

## Documentation
Take a look at the [documentation](https://www.pwenker.com/chessli) (also available [here](https://www.pwenker.com/posts/chess/chessli/home/)) to get yourself started!
Feel free to open an [issue](https://github.com/pwenker/chessli/issues/new) if you have any problems, questions or ideas :) !


## Features

- **Automatically fetch your games** and played tactics puzzles from [`lichess`](https://www.lichess.org) via the [`berserk`](https://github.com/rhgrant10/berserk) python client for the Lichess API.!
- **Find your mistakes** by parsing your games and analysing them with [`python-chess`](https://github.com/niklasf/python-chess).
- **Create a simple opening repertoire**!
- **Spaced repetition & Retrieval Practice**: Automatically  (via [`apy`](https://github.com/lervag/apy)) add your game mistakes, your openings and your tackled lichess puzzles to [`Anki`](https://apps.ankiweb.net/).
- More features on the way...!


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

### Youtube-Video: CLI Demo

[![Chessli CLI Demo](https://img.youtube.com/vi/XbD71Kq7cx4/0.jpg)](https://www.youtube.com/embed/XbD71Kq7cx4)

There is also a short video showing the `chessli`s Anki cards in action:

### Youtube-Video: Anki Cards Demo
[![Chessli Anki Cards Demo](https://img.youtube.com/vi/aj-FqJhPyyA/0.jpg)](https://www.youtube.com/embed/aj-FqJhPyyA)

## Acknowledgments

- **Lichess**:
  - A free, no-ads, open source chess server that let's everyone play chess!
  - I truly love it.
  - Think about whether to [become a patron](https://lichess.org/patron)! :)
- **Anki**:
  - A free and open-source flashcard program using spaced-repetition, a technique from cognitive science for fast and long-lasting memorization.
  - I couldn't imagine learning without it anymore.
- **Anki Cards Design**
  - The interactive chess functionality on the cards is taken from [these fantastic cards](https://ankiweb.net/shared/info/1082754005).
  - You can find a great video about those cards [here](https://www.youtube.com/watch?v=uxSP1YkfD0k&feature=youtu.be).
- **Further Awesome Tools**:
  - Most of the heavy lifting, e.g. parsing games, finding mistakes, extracting openings, etc. is done with `python-chess`.
  - The communication between `lichess` and `chessli` is done via `berserk`.
  - The CLI is built with `typer`.
  - The rich colors are made possible with `rich`.
  - The `apy` tool is used to programmatically import the chess knowledge into Anki.
  - **You should really check those tools out; each and everyone one of them is amazing.**
