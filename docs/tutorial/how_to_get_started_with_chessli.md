## How to get started with Chessli

In this section we will go through a few setup steps, to get the most out of `chessli`.
If you haven't done yet, please first follow the [install instructions](../getting_started.md) to get `chessli` on your system.

### Configuration

You can type:
```console
chessli --show-configs
```
to show the current configurations.

Here you'll see a `general config` and `user config` pertaining to the currently active user.

The general config can be used to set a default user. This is useful, because if set, you won't need
to set your user name anymore in each command.
So, for example,

```console
chessli --user DrNykterstein openings ls
```
becomes a simple
```console
chessli openings ls
```
In order to set a default user name, you'll first need to locate the general config file.
The location depends on your operating system and is chosen with the help of `appdirs`.

Just type
```console
chessli --show-paths
```
to get an idea where the general config is located. On my linux system it's located at `/home/pwenker/.config/chessli/config.yml`.
Just open it and add a line, with your user name. If your user name is `DrNykterstein`, then write
into the config file `user: DrNykterstein`.

You can check if it worked by typing again
```console
chessli --show-configs
```
and see if your user name appears in the `general config`.


Note that if you have a default user name set, but want to overwrite it temporarily, you can just
again state it in the command.

For example, if you have set `DrNykterstein` as default in your config, but enter
```console
chessli --user Zhigalko_Sergei openings ls
```
this will temporarily overwrite it.

### Lichess API Authentification

Some parts of the lichess API, for example fetching your puzzle activity, require authentification.
For this purpose, you need to get a [personal API access token](https://lichess.org/account/oauth/token).
You can put this key into the `general config`, just like we did with your default user name in the
previous section.
The syntax looks like this: `token: sdjfkdsldf23` (I made `sdjfkdsldf23` up, but
you get the idea).
For more information read the [corresponding `berserk` documentation section](https://berserk.readthedocs.io/en/master/usage.html#authenticating).

:warning: Please keep your token secure! You can think of them as passwords, that you don't want to share with anyone.


### Anki Support via `apy`

In order to directly "ankify" your mistakes, openings and tactics, you need to set up [`apy`](https://github.com/lervag/apy/).
Currently `chessli` is compatible with `apy` version 0.6.0 and `anki` version 2.1.26.
Please refer to its [install instructions](https://github.com/lervag/apy/#install-instructions) for detailed information.

:warning: Please make sure to backup your Anki database before you use this.


### Get the Chessli Anki Cards

> TODO:  <31-01-21, Pascal Wenker> >
