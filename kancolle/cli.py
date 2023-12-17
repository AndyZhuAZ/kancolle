"""Console script for kancolle."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("kancolle")
    click.echo("=" * len("kancolle"))
    click.echo("for KanColle assistant software")


if __name__ == "__main__":
    main()  # pragma: no cover
