## How to learn from your games

`Chessli` allows you to fetch your games from lichess, find the mistakes you made and make Anki
cards out of them.

### A simple workflow

A simple but powerful workflow is the following.


1. Fetch the games you have played in e.g. the last week, extract mistakes you made, convert
them into an Anki-compatible representation and store this in a `csv` file.
```console
chessli games ankify --since last-week
```

2. Open up anki and import the `csv` file.

3. Learn avoiding your mistakes with the `Chessli Games` anki cards
> TODO:  <31-01-21, Pascal Wenker> >

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
