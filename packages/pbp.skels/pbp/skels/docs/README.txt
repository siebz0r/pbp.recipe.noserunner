=================
pbp.skels package
=================

.. contents::

What is pbp.skels ?
===================

pbp.skels is a collection of templates to speed up the creation of
standardized, boiler-plate code.

See http://atomisator.ziade.org for more infos.

How to use pbp.skels ?
======================

After it has been installed, you should see the pbp templates with the
paster command::

    $ paster create --list-templates
    Available templates:
        ...
        pbp_design_doc:     A Design document
        pbp_module_doc:     A Module helper document
        pbp_package:        A namespaced package
        pbp_recipe_doc:     A recipe document
        pbp_tutorial_doc:   A Tutorial document
        ...

Just pick one and launch it with paster create -t. For example::

    $ paster create -t pbp_package my.package

