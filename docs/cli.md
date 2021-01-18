# `chessli`

**Usage**:

```console
$ chessli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--user TEXT`: Select a user name
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `games`: Fetch and show games & find and ankify...
* `lichess`: Get stats and infos from Lichess
* `openings`: Show and ankify chess openings
* `tactics`: Chessli Tactics & Puzzles

## `chessli games`

Fetch and show games & find and ankify mistakes

**Usage**:

```console
$ chessli games [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ankify`: Parse your games to find mistakes and create...
* `fetch`: Fetch games from Lichess
* `ls`: List your games

### `chessli games ankify`

Parse your games to find mistakes and create Anki cards

**Usage**:

```console
$ chessli games ankify [OPTIONS]
```

**Options**:

* `--new-games-only / --no-new-games-only`: Fetch new games and only ankify those  [default: True]
* `--since [last_time|yesterday|one_hour|last_week|forever]`: [default: last_time]
* `--help`: Show this message and exit.

### `chessli games fetch`

Fetch games from Lichess

**Usage**:

```console
$ chessli games fetch [OPTIONS]
```

**Options**:

* `--perf-type [antichess|atomic|chess960|crazyhouse|horde|kingOfTheHill|racingKings|threeCheck|bullet|blitz|rapid|classical|ultraBullet]`: Select which type of games should be fetched
* `--since [last_time|yesterday|one_hour|last_week|forever]`: Select to fetch all games played 'since'  [default: last_time]
* `--help`: Show this message and exit.

### `chessli games ls`

List your games

**Usage**:

```console
$ chessli games ls [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `chessli lichess`

Get stats and infos from Lichess

**Usage**:

```console
$ chessli lichess [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `leaderboard`: Show (selected) lichess leaderboards
* `rating`: Visualize the user's rating for selected...

### `chessli lichess leaderboard`

Show (selected) lichess leaderboards

**Usage**:

```console
$ chessli lichess leaderboard [OPTIONS]
```

**Options**:

* `--type [antichess|atomic|chess960|crazyhouse|horde|kingOfTheHill|racingKings|threeCheck|bullet|blitz|rapid|classical|ultraBullet]`: Select which leaderboard you want to see
* `--help`: Show this message and exit.

### `chessli lichess rating`

Visualize the user's rating for selected chess game types

**Usage**:

```console
$ chessli lichess rating [OPTIONS]
```

**Options**:

* `--type [antichess|atomic|chess960|crazyhouse|horde|kingOfTheHill|racingKings|threeCheck|bullet|blitz|rapid|classical|ultraBullet]`: Select type for which you want to see your rating  [default: blitz]
* `--help`: Show this message and exit.

## `chessli openings`

Show and ankify chess openings

**Usage**:

```console
$ chessli openings [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ankify`: Parse your games to find new openings and...
* `ls`: List your played openings

### `chessli openings ankify`

Parse your games to find new openings and create Anki cards

**Usage**:

```console
$ chessli openings ankify [OPTIONS]
```

**Options**:

* `--new-openings-only / --no-new-openings-only`: Only ankify new openings  [default: True]
* `--since [last_time|yesterday|one_hour|last_week|forever]`: [default: last_time]
* `--help`: Show this message and exit.

### `chessli openings ls`

List your played openings

**Usage**:

```console
$ chessli openings ls [OPTIONS]
```

**Options**:

* `--eco [Volume A: Flank openings|Volume B: Semi-Open Games other than the French Defense|Volume C: Open Games and the French Defense|Volume D: Closed Games and Semi-Closed Games|Volume E: Indian Defenses]`: Limit the shown openings to specific ECO volume
* `--help`: Show this message and exit.

## `chessli tactics`

Chessli Tactics & Puzzles

**Usage**:

```console
$ chessli tactics [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ankify`: Optionally fetch new puzzles and ankify them
* `ls`: Print a pretty table of the newly played...

### `chessli tactics ankify`

Optionally fetch new puzzles and ankify them

**Usage**:

```console
$ chessli tactics ankify [OPTIONS]
```

**Options**:

* `--fetch / --no-fetch`: Select whether to fetch new puzzles before ankifying  [default: True]
* `--help`: Show this message and exit.

### `chessli tactics ls`

Print a pretty table of the newly played puzzles

**Usage**:

```console
$ chessli tactics ls [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
