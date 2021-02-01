---
date: 2021-01-20
menu:
  sidebar:
    name: "Learn Tactics"
    identifier: chessli-tutorial-tactics
    parent: chessli-tutorial
    weight: 3
---

## How to learn tactics

`chessli` allows you to fetch the lichess puzzles you played!

Lichess new tactics puzzles amount to more than one million puzzles!
These are neatly organized into different [themes](https://lichess.org/training/themes).

:information source: Lichess recently added a lot of awesome functionality.
For example, it provides
a `puzzle dashboard`, overviews about your areas you should improve and your strengths, and many
more.
Quite recently even a [`puzzle storm`](https://lichess.org/storm) was added!

### A simple workflow

A simple but powerful workflow is the following.

1. Fetch the new puzzles you have played, compare them with the puzzles you already have played before, and export only the new puzzles as anki cards in `csv` format:
```console
chessli tactics ankify
```

2. Open up anki and import the `csv` file.

3. Learn your tactics with the `Chessli Tactics` anki cards.
(Click [here](how_to_use_chesslis_anki_cards.md) relevant tutorial section on how to use the anki cards)

Note: The next time you ankify your openings, you can type:

### Customized workflow

There  more options you can choose from, type:
```console
chessli tactics --help
```
to get an overview about all possible customization options.
