import os
import secrets

class Base:
    FLASK_APP = os.environ.get("FLASK_APP")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(16)

class Development(Base):
    FLASK_ENV = os.environ.get("FLASK_ENV")
    DATABASE = os.environ.get("DATABASE")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

class Staging(Base):
    DATABASE = "steve"
    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "12345"
    SQLALCHEMY_DATABASE_URI= "postgresql://postgres:12345@localhost:5432/steve"

class Production(Base):
    pass

# Set the environment variable to choose the configuration
# Example usage: export FLASK_ENV=Development
# Default: Development
env = os.environ.get("FLASK_ENV", "Development")

if env == "Development":
    config = Development()
elif env == "Staging":
    config = Staging()
elif env == "Production":
    config = Production()
else:
    raise ValueError(f"Invalid FLASK_ENV value: {env}")

# PostgreSQL connection settings
db_host = "localhost"
db_name = "steve"
db_user = "postgres"
db_password = "12345"
db_uri = "postgresql://postgres:12345@localhost:5432/steve"
