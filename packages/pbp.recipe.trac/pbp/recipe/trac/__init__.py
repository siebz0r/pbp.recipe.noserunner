# -*- coding: utf-8 -*-
"""Recipe trac"""
import os
from os.path import join
import sys
import subprocess
import ConfigParser

import pkg_resources
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
                entry_points, pkg_resources.working_set,
                options['executable'], options['bin-directory']
                )

        # now generating the trac instance, if required
        location = options['location'] 
        project_name = options.get('project-name', 'My project')
        project_name = '"%s"' % project_name
        project_url = options.get('project-url', 'http://example.com')
        db = 'sqlite:%s' % join('db', 'trac.db')
        repos_type = options['repos-type']
        repos_path = options['repos-path']
        if not os.path.exists(location):
            os.mkdir(location)
            
        trac_admin = join(options['bin-directory'], 'trac-admin')
        
        subprocess.call([trac_admin, location, 'initenv', project_name, 
                         db, repos_type, repos_path])

        
        # if 'hg' in thr repository type, hook its plugin
        if repos_type == 'hg':
            trac_ini = join(location, 'conf', 'trac.ini') 
            parser = ConfigParser.ConfigParser()
            parser.read([trac_ini])
            if 'components' not in parser.sections():
                parser.add_section('components')
            parser.set('components', 'tracext.hg.*', 'enabled')
            parser.write(open(trac_ini, 'w'))
 
        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return tuple()
    
    update = install

