from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from atomisator.db.mappers import Base 

metadata = Base.metadata

session = None

def create_session(SQLURI, global_session=True):
    engine = create_engine(SQLURI)
    metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
    if global_session:
        global session
        session = Session()
        return session
    else:
        return Session()

def save(obj):
    session.save(obj)

def commit():
    session.commit()

def query(mapper):
    return session.query(mapper)

