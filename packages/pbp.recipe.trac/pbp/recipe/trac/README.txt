Supported options
=================

The recipe supports the following options:

``project-name``

  Default value: ``My project``.

``project-description``

  Description of the project.

``project-url``

  This URL will be used as the link on the header logo. Default value:
  ``http://example.com``.

``repos-type``

  Supported values: ``svn`` for Subversion, ``hg`` for Mercurial.

``repos-path``

  Location, on the local file system, of your code repository.

``buildbot-url``

  Add a `buildbot` item in the Trac toolbar pointing to the URL provided.

``header-logo``

  Location of the logo that will replace the default Trac logo at the top of
  each page. The file will be copied by the recipe to the ``htdocs`` directory
  of your Trac instance.

``smtp-server``

  Server used to send notification mails.

``smtp-port``

  Port to use on the mail server.

``smtp-from``

  The mail address from which notification mails appears to be sent from.

``smtp-replyto``

  The mail address that will be used if you try to reply to mail notifications.


Example usage
=============

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = trac
    ... index = http://pypi.python.org/simple
    ...
    ... [trac]
    ... recipe = pbp.recipe.trac
    ... project-name = My project
    ... project-url = http://example.com
    ... repos-type = hg
    ... repos-path = sqlite:${buildout:directory}/var/svn
    ... buildbot-url = http://buildbot.example.com
    ... header-logo = ${buildout:directory}/my_logo
    ... smtp-server = localhost
    ... smtp-port = 25
    ... smtp-from = tarek@ziade.org
    ... smtp-replyto = tarek@ziade.org
    ... """)

Let's run the buildout::

    >>> res = system(buildout)

This creates a trac instance::

    >>> ls(join(sample_buildout, 'parts', 'trac'))
    -  README
    -  VERSION
    d  attachments
    d  conf
    d  db
    d  htdocs
    d  log
    d  plugins
    d  templates

With a trac.ini file. Let's check its content::

    >>> f = join(sample_buildout, 'parts', 'trac', 'conf', 'trac.ini')
    >>> from ConfigParser import ConfigParser
    >>> parser = ConfigParser()
    >>> null = parser.read([f])
    >>> parser.get('trac', 'repository_type')
    'hg'
    >>> parser.get('trac', 'repository_dir')
    '/sample-buildout/var/svn'
    >>> parser.get('project', 'descr')
    'My example project'
    >>> parser.get('project', 'name')
    'My project'
    >>> parser.get('project', 'url')
    ''
    >>> parser.get('components', 'tracext.hg.*')
    'enabled'

    >>> parser.get('navadd', 'buildbot.url')
    'http://buildbot.example.com'


Support
=======

- Documentation: http://pypi.python.org/pypi/pbp.recipe.trac

- Bug tracker: http://bitbucket.org/tarek/atomisator/issues

- Source: http://bitbucket.org/tarek/atomisator/src/tip/packages/pbp.recipe.trac/

- pbp.recipe.trac is a sub-project of atomistor: http://atomisator.ziade.org


