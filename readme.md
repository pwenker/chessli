
# Chessli

![GitHub Repo
stars](https://img.shields.io/github/stars/pwenker/chessli?style=social)
![GitHub code size in
bytes](https://img.shields.io/github/languages/code-size/pwenker/chessli)
![Lines of
code](https://img.shields.io/tokei/lines/github/pwenker/chessli)
![GitHub last
commit](https://img.shields.io/github/last-commit/pwenker/chessli)
![GitHub
issues](https://img.shields.io/github/issues-raw/pwenker/chessli)
![GitHub
followers](https://img.shields.io/github/followers/pwenker?style=social)

![Thumbnail](https://github.com/pwenker/chessli/blob/main/imgs/chessli.png?raw=true)

***A free and open-source CHESS improvement program that combines the power
of Lichess and Anki.***

## Demos

### CLI Demo (watch whole video on [Youtube](https://www.youtube.com/embed/XbD71Kq7cx4))

![CLI DEMO GIF](https://github.com/pwenker/chessli/blob/main/imgs/chessli_cli_demo.gif?raw=true)

### Anki Cards Demo (watch whole video on [Youtube](https://www.youtube.com/embed/aj-FqJhPyyA))

![CLI CARDS GIF](https://github.com/pwenker/chessli/blob/main/imgs/chessli_cards_demo.gif?raw=true)

## Documentation
If you have a question please first take a look at the [documentation](https://www.pwenker.com/posts/chess/chessli/home/) (also available [here](https://www.pwenker.com/chessli)), which is currently work in progress.
Feel free to open an [issue](https://github.com/pwenker/chessli/issues/new) afterwards :).


## Features

- **Automatically fetch your games** and played tactics puzzles from [`lichess`](https://www.lichess.org) via the [`berserk`](https://github.com/rhgrant10/berserk) python client for the Lichess API.!
- **Find your mistakes** by parsing your games and analysing them with [`python-chess`](https://github.com/niklasf/python-chess).
- **Create a simple opening repertoire**!
- **Spaced repetition & Retrieval Practice**: Automatically  (via [`apy`](https://github.com/lervag/apy)) add your game mistakes, your openings and your tackled lichess puzzles to [`Anki`](https://apps.ankiweb.net/).
- More features on the way...!


## Getting Started
:information_source: **Information**
- At the moment, some technical expertise is needed to use `Chessli`.
- Starting with version 0.2, however, I will add an Anki-Addon to ease those technical hurdles.
- Also, please notice that this is a very early version, and some code parts are still rough on the edges.
- Further, there are still some opinionated parts and hard-coded choices:
  - For example, it is not possible to fetch more than 20 games at once (to not bug down Lichess).
  - A lot more options are going to be opened up as soon as the codebase stabilises.
- *Long story short*: things will improve over time! But feel free to open up issues!

### Get Chessli

1. Clone this repository & navigate into it:

```console
git clone https://github.com/pwenker/chessli.git && cd chessli
```

2. Install chessli with `pip`:

```console
pip install -e .
```

### Anki Support via `apy`

- In order to directly "ankify" your mistakes, openings and tactics, you need to set up [`apy`](https://github.com/lervag/apy/).
- Currently `chessli` is compatible with `apy` version 0.6.0 and `anki` version 2.1.26.
- Please refer to its [install instructions](https://github.com/lervag/apy/#install-instructions) for detailed information.

### Lichess API Authentification

- Some parts of the lichess API, for example fetching your puzzle activity, require authentification.
- For this purpose, you need to get a [personal API access token](https://lichess.org/account/oauth/token).  Put your token into `configs/lichess.token`.
- For more information read the [corresponding `berserk` documentation section](https://berserk.readthedocs.io/en/master/usage.html#authenticating).

### Get the Chessli Anki Cards

- There is no dedicated shared deck page on Anki available yet, but will be coming soon.
- Until then, download the required sample of Anki cards from [here]("/imgs/Chessli Sample Cards.apkg").

*Acknowledgments*:

- The interactive chess functionality on the cards is taken from [these fantastic cards](https://ankiweb.net/shared/info/1082754005).
- You can find a great video about those cards [here](https://www.youtube.com/watch?v=uxSP1YkfD0k&feature=youtu.be).


## Basic Usage
To get an overview of the basic CLI capabilities of `Chessli`, take a look at this short demo video I
created (click on the image below to watch on youtube):

### Youtube-Video: CLI Demo
[![Chessli CLI Demo](https://img.youtube.com/vi/XbD71Kq7cx4/0.jpg)](https://www.youtube.com/embed/XbD71Kq7cx4)

There is also a short video showing the `chessli`s Anki cards in action:

### Youtube-Video: Anki Cards Demo
[![Chessli Anki Cards Demo](https://img.youtube.com/vi/aj-FqJhPyyA/0.jpg)](https://www.youtube.com/embed/aj-FqJhPyyA)

:information_source: I am in the midst of creating a comprehensive documentation that will be released with version 0.2.

Until then you can take a look at the [CLI documentation](docs/cli.md), or programmatically ask it questions:

**Examples**:

- Getting general help for `chessli`:

```console
chessli --help
```
- Getting help for individual `chessli` commands:

```console
chessli games --help
```

- You can add a create a file `configs/lichess.user` and put your user name in it.
- Then it will be used as default username in place of mighty `DrNykterstein`.

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
