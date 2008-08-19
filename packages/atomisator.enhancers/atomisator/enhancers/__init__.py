import digg

TPML = """\
<div>
  <strong>%s</strong>
  <ul>
    %s
  </ul>
</div>
"""

LI = """\
     <li>%s</li>
"""         

class DiggComments(object):
    """
    Will check on Digg of the story
    has been digged. If so, displays
    user comments at the end of the entry.
    """
    def __call__(self, entry, digg_id='http://example.com'):
        url = entry.url 
        server = digg.Digg(digg_id)
        try:
            stories = server.getStories(link=url)
        except (digg.Digg.Error, IOError):
            return entry
        if stories == []:
            return entry
        id_ = stories[0].id
        comments = server.getStoriesComments(id_)
        comments = [LI % c.content for c in comments]
        comments = TPML % ('Digg comments', '\n'.join(comments))
        entry.summary = entry.summary + comments
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
    def prepare(self, entries):
        # preparing data
        self._tags = {}
        self._links = {}
        for e in entries:
            for vals, rel in ((e.links, self._links), (e.tags, self._tags)):
                for v in vals:
                    if v not in rel:
                        rel[v] = [e]
                    elif e not in rel[v]:
                        rel[v].append(e)
            
    def __call__(self, entry):
        
        related = []

        for vals, rel in ((entry.tags, self._tags), (entry.links, self._links)):
            for val in vals:
                if val in rel:
                    for e in rel[val]:
                        if e not in related and e.id != entry.id:
                            related.append(e)
        if related != []:
            related = [LI % r.url for r in related]
            related = TPML % ('Related', '\n'.join(related))
            entry.summary = entry.summary + related
        return entry


