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
    def __call__(self, entry, entries, digg_id='http://example.com'):
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
    def __call__(self, entry, entries):
        related = []
        tags = set(entry.tags)
        links = set(entry.links)       
        def _inside(elements, sources):
            for e in elements:
                if e in sources:
                    return True
            return False

        for e in entries:
            # by tags or links
            if _inside(e.tags, tags) or _inside(e.links, links):

                related.append(e)

        if related != []:
            related = [LI % r.url for r in related]
            related = TPML % ('Related', '\n'.join(related))
        entry.summary = entry.summary + related
        return entry


