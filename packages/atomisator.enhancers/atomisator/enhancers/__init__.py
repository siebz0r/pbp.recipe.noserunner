import digg

COMMENTS = """\
<div>
  <h1>Digg comments</h1>
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
        stories = server.getStories(link=url)
        if stories == []:
            return entry
        id_ = stories[0].id
        comments = server.getStoriesComments(id_)
        comments = [LI % c.content for c in comments]
        entry.summary = entry.summary + COMMENTS % comments

        return entry

