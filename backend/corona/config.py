"""Default configuration

Use env var to override
"""
import os

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

# Get Postgres environment data
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_URL = os.getenv('POSTGRES_URL')
POSTGRES_DB = os.getenv('POSTGRES_DB')

# Build SQLalchemy URI
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DB}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT configuration
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
PROPAGATE_EXCEPTIONS = True
