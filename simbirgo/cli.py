import typer

from . import monolit


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.add_typer(monolit.get_cli(), name="monolit")

    return cli
