Supported options
=================

The recipe supports the following options:

.. Note to recipe author!
   ----------------------
   For each option the recipe uses you shoud include a description
   about the purpose of the option, the format and semantics of the
   values it accepts, whether it is mandatory or optional and what the
   default value is if it is omitted.

option1
    Description for ``option1``...

option2
    Description for ``option2``...


Example usage
=============

.. Note to recipe author!
   ----------------------
   zc.buildout provides a nice testing environment which makes it
   relatively easy to write doctests that both demonstrate the use of
   the recipe and test it.
   You can find examples of recipe doctests from the PyPI, e.g.

     http://pypi.python.org/pypi/zc.recipe.egg

   The PyPI page for zc.buildout contains documentation about the test
   environment.

     http://pypi.python.org/pypi/zc.buildout#testing-support

   Below is a skeleton doctest that you can start with when building
   your own tests.

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

