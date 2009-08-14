============
atomistor.db
============

This package provides a few mappers to store feed entries
in a SQL database.

The SQL uri is provided in the config module::

    >>> from atomisator.db.session import create_session
    >>> create_session('sqlite:///:memory:')
    <sqlalchemy.orm.session.Session object at ...>

Let's create an entry::

    >>> from atomisator.db.core import create_entry
    >>> entry = {'link': 'http://www.python.org/news',
    ...          'summary': 'Summary goes here',
    ...          'title': 'Python 2.6alpha1 and 3.0alpha3 released',
    ...          'links': ['http://www.python.org'],
    ...          'tags': [{'term':'cool'}, {'term':'fun'}]}
    >>> id_, e = create_entry(entry)
    >>> type(id_)
    <type 'int'>

We get the database id back. Now let's look for entries::

    >>> from atomisator.db.core import get_entries
    >>> entries = get_entries()  # returns a generator object
    >>> entries[0]
    <Entry('Python 2.6alpha1 and 3.0alpha3 released')>

Some filtering can be done ::

    >>> entries = get_entries(link='http://www.python.org/news')
    >>> list(entries)
    [<Entry('Python 2.6alpha1 and 3.0alpha3 released')>]


    >>> entries = get_entries(link='xxxx')
    >>> list(entries)
    []

