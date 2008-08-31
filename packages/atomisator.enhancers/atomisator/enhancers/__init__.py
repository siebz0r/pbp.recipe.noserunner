# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
#
import digg
import BeautifulSoup
import re

options = re.DOTALL | re.UNICODE | re.MULTILINE | re.IGNORECASE
ABSOLUTE = re.compile(r'^(ftp|http|https)://', options)

TPML = """\
<br/><br/>
<div>
  <strong>%s</strong>
  <ul>
    %s
  </ul>
</div>
"""

LI = """\
     <li><a href="%s">%s</a></li>
"""       

LI_COMMENT = """\
     <li>%s</li>
"""         

class ShowTags(object):
    """
    Will display tags.
    """
    def __call__(self, entry):
        if entry.tags == []:
            return entry
        tags = [LI % t for t in entry.tags]
        tags = TPML % ('tags', '\n'.join(tags))
        entry.summary = entry.summary + tags
        return entry

class DiggComments(object):
    """
    Will check on Digg of the story
    has been digged. If so, displays
    user comments at the end of the entry.
    """
    def __call__(self, entry, digg_id='http://example.com'):
        link = entry.link 
        server = digg.Digg(digg_id)
        try:
            stories = server.getStories(link=link)
        except (digg.Digg.Error, IOError):
            return entry
        if stories == []:
            return entry
        id_ = stories[0].id
        try:
            diggs = len(server.getStoryDiggs(id_))
        except (digg.Digg.Error, IOError):
            diggs = 0

        entry.title = '%s - Digged !' % entry.title

        header = '<div><strong>%d</strong> Diggs</div><br/>' % diggs
        comments = server.getStoriesComments(id_)
        if len(comments) > 0:
            comments = [LI_COMMENT % c.content for c in comments]
            comments = TPML % ('Digg comments', '\n'.join(comments))
        else:
            comments = ''

        if entry.summary is None:
            entry.summary = header + comments
        else:
            entry.summary = header + entry.summary + comments
        
        return entry

class RelatedEntries(object):
    """
    Will add a list of links
    at the end with a link to all related 
    entries.

    One entry relates to another one if it has at least
    one of this common pattern:
    
        - two common tags or link
        - links to the same page            XXX TODO
        - its Leventstein distance is small XXX TODO
    """
    

    def _get_page_links(self, url):
        """return links found in the page"""
        
        try:
            page = urllib2.urlopen(link)
            if 'content-type' in page.headers.keys():
                content_type = page.headers['content-type'].split(';')
                type_ = content_type[0].strip().lower()
                if type_ not in ('text/html', 'text/plain', 'test/rst'):
                    return []
            url_content = page.read()
        except urllib2.HTTPError:
            return []

        return self._get_content_link(content)

    def _get_content_link(self, content):
        """extract content"""
        if content is None:
            return []
        
        s = BeautifulSoup.BeautifulSoup(content)  
        def _href(a):
            attrs = dict(a.attrs)
            href = attrs.get('href')
            if href is None:
                return False
            return ABSOLUTE.search(href) is not None and href

        links = []
        for a in s.findAll('a'):
            href = _href(a)
            if href and href not in links:
                links.append(href)
        return set(links) 

    def prepare(self, entries):
        # preparing data
        self._tags = {}
        self._links = {}
        for e in entries:
            links = self._get_content_link(e.summary) 
            # see if we want to do this as well
            #links = links + self._get_page_links(e.link)
            for l in links:
                if l not in self._links:
                    self._links[l] = [e]
                elif e not in self._links[l]:
                    self._links[l].append(e)

            for vals, rel in ((e.links, self._links), 
                              (e.tags, self._tags)):
                for v in vals:
                    if v not in rel:
                        rel[v] = [e]
                    elif e not in rel[v]:
                        rel[v].append(e)
            
    def __call__(self, entry):
        
        related = []
        links = [l for l in entry.links]
        for l in self._get_content_link(entry.summary):
            links.append(l)

        for vals, rel in ((entry.tags, self._tags), (links, self._links)):
            if vals is None:
                continue
            for val in vals:
                if val in rel:
                    for e in rel[val]:
                        if e not in related and e.id != entry.id:
                            related.append(e)
        if related != []:
            related = [LI % (r.link, r.title) for r in related]
            related = TPML % ('Related', '\n'.join(related))
            entry.summary = entry.summary + related
        return entry


