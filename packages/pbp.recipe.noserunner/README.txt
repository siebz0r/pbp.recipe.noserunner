This package is part of the `Expert Python Programming` book  written by
Tarek Ziadé.


For more information, go to http://atomisator.ziade.org

.. contents::

QuickStart
**********

`pbp.recipe.noserunner` will let you create a `Nose` test runner script in 
your buildout. Here's an example of the simplest configuration::

    [buildout]
    parts = test

    [test]
    recipe = pbp.recipe.noserunner

If you run the builout, a `test` script will be created in the bin directory to
run your tests using Nose.

Links: 

- Nose project : http://somethingaboutorange.com/mrl/projects/nose
- zc.buildout : http://pypi.python.org/pypi/zc.buildout

