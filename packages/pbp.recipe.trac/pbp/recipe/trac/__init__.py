# -*- coding: utf-8 -*-
"""Recipe trac"""

import os
from os.path import join
import sys
import subprocess
import ConfigParser
import shutil

import pkg_resources
import zc.buildout
import zc.recipe.egg

from trac.admin.console import TracAdmin
from trac.ticket.model import *
from trac.perm import PermissionSystem



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

        # Utility function to interpreted boolean option value
        getBool = lambda s: s.strip().lower() in ['true', 'yes']

        # Utility function to parse a multi-line/multi-value parameter
        def cleanMultiParams(v):
            params = [s.split('|') for s in [l.strip() for l in v.split('\n')] if len(s) > 0]
            cleaned_params = []
            for line in params:
                cleaned_params.append([row.strip() for row in line])
            return cleaned_params

        # Utility function to transform any string to an ID
        getId = lambda s: ''.join([c for c in s if c.isalnum()]).lower()

        options = self.options

        # Add command line scripts trac-admin and tracd into bin
        entry_points = [('trac-admin', 'trac.admin.console', 'run'),
                        ('tracd', 'trac.web.standalone', 'main')]
        zc.buildout.easy_install.scripts(
                entry_points, pkg_resources.working_set,
                options['executable'], options['bin-directory']
                )


        ####################
        # Init Trac instance
        ####################

        # Generate the trac instance, if required
        location = options['location']
        project_name = options.get('project-name', 'My project')
        project_url = options.get('project-url', 'http://example.com')
        db = 'sqlite:%s' % join('db', 'trac.db')
        repos_type = options['repos-type']
        repos_path = options['repos-path']
        if not os.path.exists(location):
            os.mkdir(location)
        trac = TracAdmin(location)
        if not trac.env_check():
            trac.do_initenv('"%s" %s %s %s' % (project_name, db, repos_type, repos_path))
        env = trac.env

        # Remove Trac default example data
        clean_up = getBool(options.get('remove-examples', 'True'))
        if clean_up:
            # Remove default milestones
            for mil in Milestone.select(env):
                if mil.name in ['milestone1', 'milestone2', 'milestone3', 'milestone4']:
                    mil.delete()
            # Remove default components
            for comp in Component.select(env):
                if comp.name in ['component1', 'component2']:
                    comp.delete()

        # Add custom milestones
        for mil_name in cleanMultiParams(options.get('milestones', '')):
            try:
                mil = Milestone(env, name=mil_name)
            except ResourceNotFound:
                mil = Milestone(env)
                mil.name = mil_name
                mil.insert()

        # Add custom components
        for comp_data in cleanMultiParams(options.get('components', '')):
            try:
                comp = Component(env, name=comp_name)
            except ResourceNotFound:
                comp = Component(env)
                comp.name = comp_data[0]
                if len(comp_data) == 2 and comp_data[1] not in [None, '']:
                    comp.owner = comp_data[1]
                comp.insert()

        # Set custom permissions
        perm_sys = PermissionSystem(env)
        for cperm in cleanMultiParams(options.get('permissions', '')):
            if len(cperm) == 2:
                user = cperm[0]
                current_user_perms = perm_sys.get_user_permissions(user)
                perm_list = [p.upper() for p in cperm[1].split(' ') if len(p)]
                for perm in perm_list:
                    if perm not in current_user_perms:
                        perm_sys.grant_permission(user, perm)


        #######################
        # Generate the trac.ini
        #######################

        # Read the trac.ini config file
        trac_ini = join(location, 'conf', 'trac.ini')
        parser = ConfigParser.ConfigParser()
        parser.read([trac_ini])

        # Clean-up trac.ini: add missing stuff
        if 'components' not in parser.sections():
            parser.add_section('components')

        # Force upgrade of informations used during initialization
        parser.set('project', 'name', project_name)
        parser.set('trac', 'repository_dir', repos_path)
        parser.set('trac', 'repository_type', repos_type)

        # Set project description
        project_descr = options.get('project-description', None)
        if project_descr:
            parser.set('project', 'descr', project_descr)
            parser.set('header_logo', 'alt', project_descr)

        # Setup logo
        header_logo = options.get('header-logo', '')
        header_logo = os.path.realpath(header_logo)
        if os.path.exists(header_logo):
            shutil.copyfile(header_logo, join(location, 'htdocs', 'logo'))
        parser.set('header_logo', 'src', 'site/logo')
        parser.set('header_logo', 'link', project_url)

        # Set footer message
        parser.set('project', 'footer', options.get('footer-message', 'This Trac instance was generated by <a href="http://pypi.python.org/pypi/pbp.recipe.trac">pbp.recipe.trac</a>.'))

        # SMTP parameters
        for name in ('always-bcc', 'always-cc', 'default-domain', 'enabled',
                     'from', 'from-name', 'password', 'port', 'replyto',
                     'server', 'subject-prefix', 'user'):
            param_name = "smtp-%s" % name
            default_value = None
            if param_name == "smtp-from-name":
                default_value = project_name 
            value = options.get(param_name, default_value)
            if value is not None:
                parser.set('notification', name.replace('-', '_'), value)


        ###############
        # Plugins setup
        ###############

        # If 'hg' in the repository type, hook its plugin
        if repos_type == 'hg':
            parser.set('components', 'tracext.hg.*', 'enabled')

        # Configure the NavAdd plugin
        menu_items = cleanMultiParams(options.get('additional-menu-items', ''))
        item_list = []
        for item in menu_items:
            item_title = item[0]
            item_url = item[1]
            item_id = getId(item_title)
            item_list.append((item_id, item_title, item_url))
        if item_list > 0:
            parser.set('components', 'navadd.*', 'enabled')
            if 'navadd' not in parser.sections():
                parser.add_section('navadd')
            parser.set('navadd', 'add_items', ','.join([i[0] for i in item_list]))
            for (uid, title, url) in item_list:
                parser.set('navadd', '%s.target' % uid, 'mainnav')
                parser.set('navadd', '%s.title'  % uid, title)
                parser.set('navadd', '%s.url'    % uid, url)

        # Enable and setup time tracking
        time_tracking = options.get('time-tracking-plugin', 'disabled').strip().lower() == 'enabled'
        if time_tracking:
            parser.set('components', 'timingandestimationplugin.*', 'enabled')

        # Enable and setup the stat plugin
        stats = options.get('stats-plugin', 'disabled').strip().lower() == 'enabled'
        if stats:
            parser.set('components', 'tracstats.*', 'enabled')

        # Enable and setup the subversion location plugin
        if repos_type == 'svn':
            repos_url = options.get('repos-url', None)
            if repos_url:
                parser.set('components', 'subversionlocation.*', 'enabled')
                if 'svn' not in parser.sections():
                    parser.add_section('svn')
                parser.set('svn', 'repository_url', repos_url)


        #######################
        # Final upgrades & sync
        #######################

        # Apply custom parameters defined by the user
        custom_params = cleanMultiParams(options.get('trac-ini-additional', ''))
        for param in custom_params:
            if len(param) == 3:
                section = param[0]
                if section not in parser.sections():
                    parser.add_section(section)
                parser.set(section, param[1], param[2])

        # Write the final trac.ini
        parser.write(open(trac_ini, 'w'))

        # Upgrade Trac instance to keep it fresh
        needs_upgrade = env.needs_upgrade()
        force_upgrade = getBool(options.get('force-instance-upgrade', 'False'))
        if needs_upgrade or force_upgrade:
            env.upgrade(backup=True)

        # Force repository resync
        repo_resync = getBool(options.get('force-repos-resync', 'False'))
        if repo_resync:
            trac.do_resync('')

        # Upgrade default wiki pages embedded in Trac instance
        wiki_upgrade = getBool(options.get('wiki-doc-upgrade', 'False'))
        if wiki_upgrade:
            # Got the command below from trac/admin/console.py
            trac._do_wiki_load( pkg_resources.resource_filename('trac.wiki', 'default-pages')
                              , ignore=['WikiStart', 'checkwiki.py']
                              , create_only=['InterMapTxt']
                              )

        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return tuple()

    update = install

