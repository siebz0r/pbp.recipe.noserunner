from atomisator.db import session 
from atomisator.db.mappers import Entry
from atomisator.db.mappers import Entry
from atomisator.db.config import SQLURI

def create_entry(data):
    """Creates an entry in the db."""
    entry_args = {}
    for key, value in data.items():
        if key in entry.c.keys() and key != 'id':
            entry_args[key] = value
    
    new = Entry(**entry_args)

    if 'links' in data:
        new.add_links(data['links'])

    if 'tags' in data:
        new.add_tags(data['tags'])

    session.save(new)
    session.commit()
    return entry.id

def get_entries(**kw):
    """Returns entries"""
    if kw == {}:
        query = session.query(Entry)
    else:
        query = session.query(Entry).filter_by(**kw)
    for entry in query:
        yield entry

