from app.core.config import DATABASE_URL
from databases import Database
from sqlalchemy import create_engine

engine = create_engine(str(DATABASE_URL))
database = Database(str(DATABASE_URL))
