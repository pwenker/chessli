
### Tactics
- https://lichess.org/training/themes
- https://database.lichess.org/#puzzles
- https://asciinema.org/
- https://asciinema.org/connect/89935f9b-f572-4bb5-bdc3-90bd46750131

> TODO: Add short video <15-01-21, Pascal Wenker> >
- **Documentation:** 
> TODO: add link <15-01-21, Pascal Wenker> >

## Features

- Fetch your games and tackled puzzles from lichess (via Berserk)
- Find the mistakes you made in your games (via python chess & stockfish)
- Create a simple opening repertoire: neatly list the openings you have played!
- Finally, learn and remember: automatically add your game mistakes, your openings and your tackled lichess puzzles to Anki.

For more details about the features please visit [here](www.google.de).


## Set up
Some parts of the lichess API, for example fetching your puzzle activity, require authentification. For this purpose, you need to get a personal token [lichess link].
Put your token to configs/lichess.token. For more information read https://berserk.readthedocs.io/en/master/usage.html#authenticating.

## Usage

In order to use chanki, follow the following steps:

#### Add theme as git submodule

At first, clone this repository.

```console
$ git submodule add https://github.com/hugo-toha/toha.git themes/toha
```
Then use pip to install it locally
```
cd chanki && pip install -e 
```

#### Configuring the app
Now, configureto to your needs, just change the username from pwenker to yours:
```yaml
patzer: pwenker
```


## Project Roadmap

Here, are the current plan and progress of various components of this app.

### Usability
- [ ] **Anki Addon**:  Allows to pull games, puzzles and create flashcards directly from Anki, so no technical expertise is needed anymore.
- [ ] **Documentation**: Clearly show how to use the app.

### Openings
- [ ] Add cli-option thatshows the frequency of played openings 

### Games
- [ ] Add cli-option that shows some games statistics

### Studies
- [ ] Add cli subcommand that allows to fetch study information
- [ ] Add subcommand to meaninfully ankify studies (for the lichess v2 puzzle themes this is in the
  process)

## Thank you

- Lichess: Free, no-ads, open source chess server that let's everyone play chess!
- Anki: Free and open-source flashcard program using spaced-repetition, a technique from
  cognitive science for fast and long-lasting memorization.

> TODO: shortly add other programs <15-01-21, Pascal Wenker> >
