from sqlalchemy import desc  
from sqlalchemy.orm import eagerload

from atomisator.db import session 
from atomisator.db.mappers import Entry

def create_entry(data, commit=True):
    """Creates an entry in the db."""
    entry_args = {}
    for key, value in data.items():
        if key == 'link':
            entry_args['url'] = value
        elif key == 'published':
            entry_args['date'] = data['published']
        elif key in ('title_detail', 'summary_detail'):
            entry_args[key] = value['value'] 
        elif key in Entry.__table__.c.keys() and key != 'id':
            entry_args[key] = value
    
    # check it the url already exists in the database
    entries = get_entries(url=entry_args['url'])
    if entries.count() > 0:
        found_entry = entries.first()
        # yes, let's check if it has been updated
        if entry_args['updated'] == found_entry.updated:
            return found_entry.id, found_entry
        # updating it
        changed = False
        for key in Entry.__table__.c.keys():
            if key in entry_args:
                value = entry_args[key]
                if getattr(found_entry, key) != value:
                    setattr(found_entry, key, value)
                    changed = True
        if commit and changed:
            session.commit()
        return found_entry.id, found_entry

    new = Entry(**entry_args)
    if 'links' in data:
        new.add_links(data['links'])

    if 'tags' in data:
        new.add_tags(data['tags'])

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
    query = query.order_by(desc(Entry.date))
    if size is not None:
        query = query.limit(size)
    return query

