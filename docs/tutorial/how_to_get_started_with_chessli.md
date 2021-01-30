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
