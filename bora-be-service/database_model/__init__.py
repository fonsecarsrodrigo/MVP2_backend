# In Python, a __init__.py file marks a directory as a package
# and controls how that package is initialized and exposed.
# Without __init__.py (in older Python versions), this import would fail.

from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pathlib import Path

# importing the elements defined in the model
# Need to import models to ensure they are added do DB
from database_model.base import Base
from database_model.Customer import Customer
from database_model.TravelPlan import TravelPlan

ROOT_DIR = Path(__file__).resolve().parent
db_path = ROOT_DIR / "database"
# Ensure the database directory exists
db_path.mkdir(parents=True, exist_ok=True)

# database access URL (this is a local SQLite access URL)
db_url = f"sqlite:///{(db_path / 'db.sqlite3').as_posix()}"

# create the database connection engine
engine = create_engine(db_url, echo=False)

# Instantiate a session creator bound to the database
Session = sessionmaker(bind=engine)

# create the database if it does not exist
if not database_exists(engine.url):
    create_database(engine.url)

# create the database tables if they do not exist
Base.metadata.create_all(engine)
