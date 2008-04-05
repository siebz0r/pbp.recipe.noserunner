# -*- coding: utf-8 -*-
"""Recipe trac"""
import os
import sys

import zc.buildout
import zc.recipe.egg

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'],
            self.name,
            )
        options['bin-directory'] = buildout['buildout']['bin-directory']
        options['executable'] = sys.executable
 
    def install(self):
        """Installer"""
        options = self.options
        # adding trac-admin and tracd into bin
        entry_points = [('trac-admin', 'trac.admin.console', 'run'), 
                        ('tracd', 'trac.web.standalone', 'main')]
        
        zc.buildout.easy_install.scripts(
                entry_points,
                {}, options['executable'], options['bin-directory'],
                )

        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return tuple()
    
    update = install

