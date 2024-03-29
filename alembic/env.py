from logging.config import fileConfig
import os
# from dotenv import load_dotenv # for dev
from sqlalchemy import create_engine

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    # load_dotenv() # for dev when not in container
    dbType = os.environ.get("ECHO_DB_TYPE")
    if dbType is None or dbType == "sqlite":
        return 'sqlite:///data/database.db'
    elif dbType == "mysql":
        dbUser = os.environ.get("ECHO_MYSQL_USER")
        dbHost = os.environ.get("ECHO_MYSQL_HOST")
        dbPass = os.environ.get("ECHO_MYSQL_PASS")
        dbName = os.environ.get("ECHO_MYSQL_DB")
        return "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbUser, dbPass, dbHost, dbName)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    connectable = create_engine(get_url())

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
