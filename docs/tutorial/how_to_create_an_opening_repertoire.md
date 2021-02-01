## How to learn from your games

### A simple workflow

A simple but powerful workflow is the following.

1. Fetch the games you have played, in e.g. the last week, extract the openings, and export them as anki cards in `csv` format:
```console
chessli openings ankify --since last-week
```

2. Open up anki and import the `csv` file.

3. Learn your openings with the `Chessli Openings` anki cards.
(Click [here](how_to_use_chesslis_anki_cards.md) relevant tutorial section on how to use the anki cards)

Note: The next time you ankify your openings, you can type:

```console
chessli openings ankify --since last-time
```
or just
```console
chessli openings ankify
```
(chessli will use `--since last-time` per default).
This way you always fetch the newly played games.

### Show your openings

You can get a nice overview of your known openings with:
```console
chessli openings ls
```

Check
```console
chessli openings ls --help
```
to get to know all the customization options.

For example,
```console
chessli openings ls --eco D
```
will show only those of your openings that belong to the ECO Volume D, which are  closed games and semi-closed games.


### Customized workflow

There are a lot more options you can choose from, type:
```console
chessli openings --help
```
to get an overview about all possible customization options.
