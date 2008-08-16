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
    
    def __call__(self, entry):
        url = entry.url 
        server = digg.Digg('http://example.com')
        try:
            stories = server.getStories(link=url)
        except digg.Digg.Error:
            return entry
        if stories == []:
            return entry
        id_ = stories[0].id
        comments = server.getStoriesComments(id_)
        comments = [LI % c.content for c in comments]
        entry.summary = entry.summary + COMMENTS % '\n'.join(comments)

        return entry

