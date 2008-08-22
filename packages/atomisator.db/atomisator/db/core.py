from sqlalchemy import desc  
from sqlalchemy.orm import eagerload

from atomisator.db import session 
from atomisator.db.mappers import Entry

def create_entry(data, commit=True):
    """Creates an entry in the db."""
    link = data['link']

    if 'id' in data:
        del data['id']
    for key in ('title_detail', 'summary_detail'):
        if key not in data:
            continue
        data[key] = data[key]['value']

    # check it the url already exists in the database
    entries = get_entries(link=link)
    
    if entries.count() > 0:
        found_entry = entries.first()
        # yes, let's check if it has been updated
        if 'updated' in data and data['updated'] == found_entry.updated:
            return found_entry.id, found_entry
        # updating it
        changed = found_entry.update(**data)
        if commit: # and changed:
            session.commit()
        return found_entry.id, found_entry
    
    new = Entry(**data)
    #if 'links' in data:
    #    new.add_links(data['links'])

    #if 'tags' in data:
    #    new.add_tags(data['tags'])

    session.save(new)
    if commit:
        session.commit()
    return new.id, new

def get_entries(size=None, **kw):
    """Returns entries"""
    if kw == {}:
        query = session.query(Entry)
    else:
        query = session.query(Entry).filter_by(**kw)

    query = query.options(eagerload('links'), eagerload('tags'))
    query = query.order_by(desc(Entry.updated))
    if size is not None:
        query = query.limit(size)
    return query

