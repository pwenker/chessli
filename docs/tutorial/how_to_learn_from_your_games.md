## How to learn from your games

`Chessli` allows you to fetch your games from lichess, find the mistakes you made and then create Anki cards out of them.

!!! note
    In order for `chessli` to find your mistakes you first need to perform a computer analysis on lichess via the analysis board.

### A simple workflow

A simple but powerful workflow is the following.

1. Fetch the games you have played in e.g. the last week, extract mistakes you made, and convert them as anki cards in `csv` format:
```console
chessli games ankify --since last-week
```

2. Open up anki and import the `csv` file.

3. Learn from your mistkes with the `Chessli Games` anki cards.
(Click [here](how_to_use_chesslis_anki_cards.md) relevant tutorial section on how to use the anki cards)

Note: The next time you fetch your games, you can type:

```console
chessli games ankify --since last-time
```
or just
```console
chessli games ankify
```
(chessli it will use `--since last-time` per default).
This way you always fetch the newly played games.

### Customized workflow

There are a lot of options you can choose, type:
```console
chessli games --help
```
and
```console
chessli games ankify --help
```
to get an overview about all possible customization options.

#### Example
For example you might want to only ankify the mistakes of `classical` and `rapid` games that you
played in the last week and limit the number of games to `5`, in order to make the workload more manageable:

```console
chessli games ankify --since last-week --perf-type blitz --perf-type classical --max 5
```
