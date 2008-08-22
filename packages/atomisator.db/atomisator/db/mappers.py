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

from datetime import datetime

Base = declarative_base()

class Entry(Base):

    __tablename__ = 'atomisator_entry'
    id = Column(Integer, primary_key=True)
    link = Column(Text())
    date = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now)
    summary = Column(UnicodeText())
    summary_detail = Column('summary_detail', UnicodeText())
    title = Column(UnicodeText())
    title_detail = Column(UnicodeText())    
    
    links = relation("Link", order_by="Link.id", backref="entry")
    tags = relation("Tag", order_by="Tag.id", backref="entry")

    def __init__(self, **kw):
        self.update(**kw)

    def update(self, **kw):
        if 'link' in kw:
            self.link = kw['link']
        if 'date' in kw:
            self.date = kw['date']
        if 'updated' in kw:
            self.updated = kw['updated']
        if 'summary' in kw:
            self.summary = kw['summary']
        if 'summary_detail' in kw:
            self.summary_detail = kw['summary_detail']
        if 'title_detail' in kw:
            self.title_detail = kw['title_detail']
        if 'title' in kw:
            self.title = kw['title']
        if 'links' in kw:
            self.add_links(kw['links'])
        if 'tags' in kw:
            self.add_tags(kw['tags'])

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

