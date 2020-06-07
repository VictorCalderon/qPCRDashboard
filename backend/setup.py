from setuptools import setup, find_packages

__version__ = "0.1"

setup(
    name="qpcr-manager",
    version=__version__,
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-restful",
        "flask-migrate",
        "flask-jwt-extended",
        "flask-marshmallow",
        "marshmallow-sqlalchemy",
        "python-dotenv",
        "passlib",
        "apispec[yaml]",
        "apispec-webframeworks",
        "pandas",
        "psycopg2-binary",
        "gunicorn",
        "scikit-learn"
    ],
    entry_points={
        "console_scripts": [
            "qpcr-manager = qpcr_manager.manage:cli"
        ]
    },
)
