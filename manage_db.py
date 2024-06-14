import click
from flask.cli import with_appcontext
from app import create_app, db
from seeds import run_seeds

app = create_app()


@click.group()
def cli():
    pass


@cli.command("seed")
@click.argument("seed_names", nargs=-1)
@with_appcontext
def seed_command(seed_names):
    """Seed the database with specified seed files."""
    run_seeds(*seed_names)


if __name__ == "__main__":
    cli()
