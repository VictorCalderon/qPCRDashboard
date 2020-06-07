import click

from getpass import getpass
from flask.cli import FlaskGroup
from qpcr_manager.app import create_app


def create_qpcr_manager(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_qpcr_manager)
def cli():
    """Main entry point
    """


@cli.command("add-user")
def add_user():
    """Add a user
    """
    from qpcr_manager.extensions import db
    from qpcr_manager.models import User

    click.echo("[INFO] Add user to app")

    user_name, email = input('Username: '), input('Email: ')
    password = getpass(prompt='Password: ')

    # Instantiate user
    user = User(username=user_name, email=email, password=password, active=True)
    db.session.add(user)
    db.session.commit()

    click.echo(f"[INFO] Created user {user_name}")


@cli.command("init")
def init():
    """Create a new admin user
    """
    from qpcr_manager.extensions import db

    try:
        click.echo('[INFO] Creating all tables...')
        db.create_all()
        click.echo('[INFO] Tables created...')

    except ValueError:
        raise '[ERROR] Could not add project'


if __name__ == "__main__":
    cli()
