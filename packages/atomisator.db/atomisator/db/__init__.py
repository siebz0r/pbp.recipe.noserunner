
def create_entry(data):
    """Creates an entry in the db."""
    from atomisator.db import session 
    from atomisator.db.mappers import entry
    from atomisator.db.mappers import Entry

    entry_args = {}
    for key, value in data.items():
        if key == 'link':
            entry_args['url'] = value
        elif key == 'published':
            entry_args['date'] = data['published']
        elif key in ('title_detail', 'summary_detail'):
            entry_args[key] = value['value'] 
        elif key in entry.c.keys() and key != 'id':
            entry_args[key] = value

    new = Entry(**entry_args)
    if 'links' in data:
        new.add_links(data['links'])

    if 'tags' in data:
        new.add_tags(data['tags'])

    session.save(new)
    session.commit()
    return new.id

def get_entries(size=None, **kw):
    """Returns entries"""
    from atomisator.db import session 
    from atomisator.db.mappers import Entry
    from sqlalchemy import desc  
    if kw == {}:
        query = session.query(Entry)
    else:
        query = session.query(Entry).filter_by(**kw)
    if size is not None:
        query.limit = size
    return query.order_by(desc(Entry.date))

