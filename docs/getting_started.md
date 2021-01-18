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
