import os
from databases import Database
from sqlalchemy import create_engine, MetaData
from weightwhat.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData()

database = Database(DATABASE_URL)
