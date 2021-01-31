import datetime
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import typer
from rich import print
from rich.console import Console

from chessli import users_client
from chessli.enums import PerfType
from chessli.utils import as_title, create_config_from_options

console = Console()
app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context,):
    """Get stats and infos from Lichess"""

    ctx.params = ctx.parent.params
    print(f"{as_title('lichess stats')}", end="\n\n")


@app.command()
def leaderboard(
    ctx: typer.Context,
    type: Optional[PerfType] = typer.Option(
        None, help="Select which leaderboard you want to see"
    ),
):
    """Show (selected) lichess leaderboards"""

    config = create_config_from_options({**ctx.parent.params, **ctx.params})

    def print_lb(type, lb):
        print(f"[bold][blue]{type.upper()}[/bold][/blue]", end="\n\n")
        for rank, who in enumerate(lb):
            username = who["username"]
            title = who.get("title", "")
            rating = who["perfs"][type]["rating"]
            progress = who["perfs"][type]["progress"]
            if int(progress) >= 0:
                progress_str = f"([green]+{progress}[/green])"
            else:
                progress_str = f"([red]{progress}[/red])"
            print(f"{rank}. {username} ({title}) {rating} {progress_str}")

    if type is not None:
        print_lb(type, users_client.get_leaderboard(type))
    else:
        for key, value in users_client.get_all_top_10().items():
            print_lb(key, value)
            print("")


@app.command()
def rating(
    ctx: typer.Context,
    type: Optional[PerfType] = typer.Option(
        "blitz", help="Select type for which you want to see your rating"
    ),
):
    """Visualize the user's rating for selected chess game types"""
    config = create_config_from_options({**ctx.parent.params, **ctx.params})
    ratings = users_client.get_rating_history(config.user)
    available_types = [rating["name"].lower() for rating in ratings]
    if type not in available_types:
        print(
            f"User '{config.user}' did not play any '{type}' games yet! Time to play! :fire:"
        )

    for rating in ratings:
        name = rating["name"]
        if type is None or type == name.lower():
            ratings = [entry.rating for entry in rating["points"]]
            dates = [
                datetime.date(year=entry.year, month=entry.month + 1, day=entry.day)
                for entry in rating["points"]
            ]

            if ratings:
                console.log(f"Plotting {config.user}`s rating for '{type}' games")
                df = pd.DataFrame(index=dates, columns=[name], data=ratings)
                sns.set_theme(style="darkgrid")
                sns.lineplot(data=df, palette="tab10", linewidth=2.5)
                plt.show()
            else:
                print(
                    f"User '{config.user}' did not play any '{type}' games yet! Time to play! :fire:"
                )
