import os
from databases import Database
from sqlalchemy import create_engine
from weightwhat.core.config import DATABASE_URL

engine = create_engine(str(DATABASE_URL))
database = Database(str(DATABASE_URL))
