import digg

COMMENTS = """\
<div>
  <strong>Digg comments</strong>
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
    def __call__(self, entry):
        url = entry.url 
        server = digg.Digg('http://example.com')
        try:
            stories = server.getStories(link=url)
        except (digg.Digg.Error, IOError):
            return entry
        if stories == []:
            return entry
        id_ = stories[0].id
        comments = server.getStoriesComments(id_)
        comments = [LI % c.content for c in comments]
        entry.summary = entry.summary + COMMENTS % '\n'.join(comments)

        return entry

class RelatedEntries(object):
    """
    Will add a list of links
    at the end with a link to all related 
    entries.

    One entry relates to another one if it has at least
    one of this common pattern:
    
        - two common buzzwords or tags
        - links to the same page
        - its Leventstein distance is small
    """
    def __call__(self, entry, entries):
        pass

