## How to set up Chessli

In this section we will go through a few setup steps, to get the most out of `chessli`.
If you haven't done yet, please first follow the [install instructions](../getting_started.md) to get `chessli` on your system.

### Configuration

#### General config and user config
You can type:
```console
chessli --user <your_lichess_username> --show-configs
```
to show the current configurations.

Here you'll see a `general config` and a `user config` pertaining to the currently active user.

#### Saving keystrokes with a default username
The `general config` can be used to set a default username. This is useful, because if set, you won't need
to set your username anymore in each command.

So, for example,

```console
chessli --user DrNykterstein openings ls
```
becomes a simple
```console
chessli openings ls
```

#### Locating chessli's configs
In order to set a default username, you'll first need to locate the `general config` file.
The location depends on your operating system and is chosen with the help of [`appdirs`](https://pypi.org/project/appdirs/).

Just type
```console
chessli --user <your_lichess_username> --show-paths
```
to get an idea where the `general config` is located. On my linux system it's living at `/home/pwenker/.config/chessli/config.yml`.

#### Setting a default username
To then set the default username, just open the `general config` and add a line with your lichess username.
If your username is `DrNykterstein`, then write into the config file

```yaml
user: DrNykterstein
```

You can check if it worked by typing again
```console
chessli --show-configs
```
and see if your username appears in the `general config`.

#### Temporarily overwriting the default username
Note that if you have a default username set, but want to overwrite it temporarily, you can just
again state it in the command.

For example, if you have set `DrNykterstein` as default in your config, but enter
```console
chessli --user pwenker openings ls
```
this will temporarily overwrite it.

### Lichess API Authentification

Some parts of the lichess API, for example fetching your puzzle activity, require authentification.
For this purpose, you need to get a [personal API access token](https://lichess.org/account/oauth/token).

You can then put this token into the `general config`, just like we did with your default username in the previous section.
The syntax looks like this:
```yaml
token: sdjfkdsldf23
```
(I made `sdjfkdsldf23` up, but you get the idea).

:warning: Please keep your token secure! You can think of them as passwords, that you don't want to share with anyone.


### Anki Support via `apy`

In order to directly "ankify" your mistakes, openings and tactics, you need to set up [`apy`](https://github.com/lervag/apy/).
Currently `chessli` is compatible with `apy` version 0.6.0 and `anki` version 2.1.26.
Please refer to `apy's` [install instructions](https://github.com/lervag/apy/#install-instructions) for detailed information.

Note, however, that you don't necessarily need `apy`. Alternatively, all `ankify` subcommands
contain a `--export-only` option which creates a `csv` file that you can manually import into Anki.

:warning: If you use `apy`, please make sure to backup your Anki database before!


### Getting Chessli's Anki Cards Templates

You'll find the `chessli` card templates [here](https://ankiweb.net/shared/info/381105186) on `ankiweb` as a `shared deck`.
Just follow the instructions there, to set them up. :)
