from sqlalchemy import Table
from sqlalchemy import DateTime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey    
from sqlalchemy import UnicodeText
from sqlalchemy import Text

from sqlalchemy.orm import relation
from sqlalchemy.orm import mapper

from time import strptime
from datetime import datetime

metadata = MetaData()

link = Table('atomisator_link', metadata,
             Column('id', Integer, primary_key=True),
             Column('url', String(300)),
             Column('atomisator_entry_id', Integer, 
                    ForeignKey('atomisator_entry.id')))

class Link(object):
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<Link('%s')>" % self.url

mapper(Link, link)

tag = Table('atomisator_tag', metadata,
            Column('id', Integer, primary_key=True),
            Column('value', String(100)),
            Column('atomisator_entry_id', Integer, 
                   ForeignKey('atomisator_entry.id')))

class Tag(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "<Tag('%s')>" % self.value

mapper(Tag, tag) 

entry = Table('atomisator_entry', metadata,
              Column('id', Integer, primary_key=True),
              Column('url', String(300)),
              Column('date', DateTime, default=datetime.now),
              Column('summary', Text()),
              Column('summary_detail', UnicodeText()),
              Column('title', UnicodeText()),
              Column('title_detail', UnicodeText()))    
              
class Entry(object):
    def __init__(self, title, url, summary='', summary_detail='',
                 title_detail='', date=None, **kw):
        self.title = title
        self.url = url
        self.summary = summary
        self.summary_detail = summary_detail
        self.title_detail = title_detail
        if date is not None:
            self.date = date.split('.')[0]
            if self.date[-1] == 'Z':
                self.date = self.date[:-1]
            self.date = strptime(self.date, '%Y-%m-%dT%H:%M:%S')
            self.date = datetime(*self.date[:6])
        for key, val in kw.items():
            setattr(self, key, val)
    
    def add_links(self, links):
        for link in links:
            self.links.append(Link(link))

    def add_tags(self, tags):
        for tag in tags:
            self.tags.append(Tag(tag['term']))

    def __repr__(self):
        return "<Entry('%s')>" % self.title

mapper(Entry, entry, properties={    
       'links':relation(Link, backref='atomisator_entry'),
       'tags':relation(Tag, backref='atomisator_entry'),
       })


