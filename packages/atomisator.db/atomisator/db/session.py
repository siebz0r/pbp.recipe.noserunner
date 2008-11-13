from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from atomisator.db.mappers import Base 

metadata = Base.metadata

session = None

def create_session(sqluri, global_=True):
    """Creates a session. 
    
    If `global` is True creates a global session variable."""

    engine = create_engine(sqluri)
    metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
    if global_:
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

def execute(*args, **kw):
    return session.execute(*args, **kw)

