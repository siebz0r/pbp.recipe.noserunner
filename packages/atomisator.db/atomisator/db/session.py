from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from atomisator.db.config import SQLURI
from atomisator.db.mappers import metadata

engine = create_engine(SQLURI)
metadata.create_all(engine)
Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
session = Session()

def save(obj):
    session.save(obj)

def commit():
    session.commit()

def query(mapper):
    return session.query(mapper)

