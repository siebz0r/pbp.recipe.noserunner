from atomisator.db import session 
from atomisator.db.mappers import Entry
from atomisator.db.config import SQLURI

def create_entry(data):
    """Creates an entry in the db."""
    entry_args = {}
    for key, value in data.items():
        if key in Entry.c.keys():
            entry_args[key] = value
    
    entry = Entry(**entry_args)

    if 'links' in data:
        entry.add_links(data['links'])

    if 'tags' in data:
        entry.add_tags(data['tags'])

    session.save(entry)
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

