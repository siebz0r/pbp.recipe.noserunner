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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, backref

from time import strptime
from datetime import datetime

Base = declarative_base()

class Entry(Base):

    __tablename__ = 'atomisator_entry'
    id = Column(Integer, primary_key=True)
    url = Column(String(300))
    date = Column(DateTime, default=datetime.now)
    summary = Column(Text())
    summary_detail = Column('summary_detail', UnicodeText())
    title = Column(UnicodeText())
    title_detail = Column(UnicodeText())    
    
    links = relation("Link", order_by="Link.id", backref="entry")
    tags = relation("Tag", order_by="Tag.id", backref="entry")

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


class Link(Base):

    __tablename__ = 'atomisator_link'
    id = Column(Integer, primary_key=True)
    url = Column(String(300))
    atomisator_entry_id = Column(Integer, ForeignKey('atomisator_entry.id'))

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<Link('%s')>" % self.url

class Tag(Base):

    __tablename__ = 'atomisator_tag'
    id = Column(Integer, primary_key=True)
    value =  Column(String(100))
    atomisator_entry_id = Column(Integer, ForeignKey('atomisator_entry.id'))

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "<Tag('%s')>" % self.value

