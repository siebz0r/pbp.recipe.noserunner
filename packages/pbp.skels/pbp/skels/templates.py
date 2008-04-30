from pbp.skels.base import var
from pbp.skels.base import get_var
from pbp.skels.base import BaseTemplate

class Recipe(BaseTemplate):
    _template_dir = 'templates/recipe'
    summary = "A recipe"
    required_templates = []
    use_cheetah = True

    vars = [
        var('title', 'Title (use a short question)', 'Title'),
        var('short_name', ('Short name use for filename '
                           '(leave blank to make it calculated)'), 
            default='recipe'),
        var('author', 'Author name', default='John Doe'),
        var('keywords', 'Space-separated keywords/tags', 'tag1 tag2')
    ]

