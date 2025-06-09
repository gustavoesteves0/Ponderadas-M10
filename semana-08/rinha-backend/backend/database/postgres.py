import os
from pathlib import Path

import databases
from dotenv import load_dotenv
from ormar import OrmarConfig
from sqlalchemy.sql.schema import MetaData

# Carregar o .env
dotenv_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path)

DATABASE_URL = os.environ.get("DATABASE_URL")
assert DATABASE_URL is not None, "DATABASE_URL is not set"

metadata = MetaData()
database = databases.Database(DATABASE_URL)

base_ormar_config = OrmarConfig(
	database=database,
	metadata=metadata
)

