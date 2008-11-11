# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
""" DB Apis
"""
from datetime import timedelta
from datetime import datetime

from sqlalchemy import desc  
from sqlalchemy.orm import eagerload
from sqlalchemy.sql.expression import delete

from atomisator.db import session as default_session
from atomisator.db.mappers import Entry

def create_entry(data, commit=True, session=default_session):
    """Creates an entry in the db."""
    link = data['link']

    if 'id' in data:
        del data['id']
    for key in ('title_detail', 'summary_detail'):
        if key not in data:
            continue
        data[key] = data[key]['value']

    # check it the url already exists in the database
    entries = get_entries(link=link, session=session)
    
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
    session.save(new)
    if commit:
        session.commit()
    return new.id, new

def purge_entries(max_age=30, session=default_session):
    """remove old entries"""
    today = datetime.now()
    oldest = today - timedelta(days=max_age)
    entry = Entry.__table__
    session.execute(delete(entry).where(entry.c.date<oldest))
    session.commit()

def get_entries(size=None, session=default_session, **kw):
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

