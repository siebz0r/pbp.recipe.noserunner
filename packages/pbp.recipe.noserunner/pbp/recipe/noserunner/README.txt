Supported options
=================

The recipe supports the following options:

eggs
    The eggs option specified a list of eggs to test given as one ore
    more setuptools requirement strings.  Each string must be given on
    a separate line.

script
    The script option gives the name of the script to generate, in the
    buildout bin directory.  Of the option isn't used, the part name
    will be used.

extra-paths
    One or more extra paths to include in the generated test script.

defaults
    The defaults option lets you specify testrunner default
    options. These are specified as Python source for an expression
    yielding a list, typically a list literal.

working-directory
    The working-directory option lets to specify a directory where the
    tests will run. The testrunner will change to this directory when
    run. If the working directory is the empty string or not specified
    at all, the recipe will create a working directory among the parts.

environment
    A set of environment variables that should be exported before
    starting the tests.

Example usage
=============

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = test
    ... index = http://download.zope.org/simple
    ...
    ... [test]
    ... recipe = pbp.recipe.noserunner
    ... eggs = pbp.recipe.noserunner
    ... """) 

Running the buildout gives us::

    >>> print 'start', system(buildout) 
    start ...
    ...
    Generated script '/sample-buildout/bin/test'.
    <BLANKLINE>

Checking the generated script::

    >>> print open(join('bin', 'test')).read()    
    #!...
    <BLANKLINE>
    import sys
    sys.path[0:0] = [
      ...
      ]
    <BLANKLINE>
    import os
    sys.argv[0] = os.path.abspath(sys.argv[0])
    os.chdir('...test')
    <BLANKLINE>
    <BLANKLINE>
    import nose.commands
    <BLANKLINE>
    if __name__ == '__main__':
        nose.commands.nosetests()
    <BLANKLINE>

