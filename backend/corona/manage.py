import click

from getpass import getpass
from flask.cli import FlaskGroup
from corona.app import create_app


def create_corona(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_corona)
def cli():
    """Main entry point
    """


@cli.command("add-user")
def add_user():
    """Add a user
    """
    from corona.extensions import db
    from corona.models import User

    click.echo("[INFO] Add user to app")

    user_name, email = input('Username: '), input('Email: ')
    password = getpass(prompt='Password: ')

    # Instantiate user
    user = User(username=user_name, email=email, password=password, active=True)
    db.session.add(user)
    db.session.commit()

    click.echo(f"[INFO] Created user {user_name}")


@cli.command('test-query')
def test_query():
    """Test a data analysis query
    """

    from corona.extensions import db

    my_query = """
    SELECT experiment_date, CAST(COUNT(CASE WHEN amp_status THEN 1 END) as decimal) / COUNT(amp_status), COUNT(DISTINCT(sample)), COUNT(DISTINCT(name))
    FROM samples AS s 
    JOIN projects as p on s.project_id = p.id 
    JOIN results as r on r.sample_id = s.id 
    JOIN markers as m on r.marker_id = m.id 
    WHERE m.marker = 'ORF1ab' 
    GROUP BY experiment_date
    """

    data = db.session.execute(my_query)

    for date, perc_infected, total_samples, total_projects in data:
        print(str(date), round(float(perc_infected), 2), int(total_samples), int(total_projects))


@cli.command("add-project")
def add_project():
    """Add a new project to the database
    """
    from corona.helpers.preprocessing import feed_qpcrs
    from corona.models import Project, User

    user = User.query.first()
    project = Project(name='SARS-CoV-2-TEST', experiment_date='2020-05-25', user=user)

    try:
        feed_qpcrs('/home/victor/DevSpace/CoronaDB/data.txt', project, user)

    except ValueError:
        raise '[ERROR] Could not add project'


@cli.command("query-qpcrs")
def query_qpcr():
    """Add a new project to the database
    """
    from corona.helpers.preprocessing import query_qpcrs
    from corona.models import Sample

    # Get sample ID
    sample_id = Sample.query.first().id

    # Parse qPCRs for that ID
    print(query_qpcrs(sample_id))


@cli.command("init")
def init():
    """Create a new admin user
    """
    from corona.extensions import db

    try:
        click.echo('[INFO] Creating all tables...')
        db.create_all()
        click.echo('[INFO] Tables created...')

    except ValueError:
        raise '[ERROR] Could not add project'


if __name__ == "__main__":
    cli()
