Grok
****

What is grok?
=============

Grok is a smashing web framework based on `Zope Toolkit`_ technology.

.. _`Zope Toolkit`: http://docs.zope.org/zopetoolkit

Grok uses the Component Architecture and builds on Zope concepts like
content objects (models), views, and adapters.  Its simplicity lies in
using **convention over configuration** and **sensible defaults** when
wiring components together.  That means neither a configuration
language like ZCML nor a lot of repetition are needed to create a web
application with grok.

You can find out much more about Grok at our http://grok.zope.org
website.

Who is grok?
============

Grok is a friendly caveman from the Stone Age.  He has a big club that
he hunts mammoths with.  He will also use this club to smash anything
he doesn't like.

"ME GROK SMASH ZCML!"

Getting grok
============

The easiest way to get started with grok is to install the
`grokproject <https://pypi.org/project/grokproject/>`_ package
(e.g. via ``pip install grokproject``) and then create a new project
area by calling the ``grokproject`` script like so::

  $ grokproject MyProject
  ... many lines of output here

This will create a project area in ``MyProject`` as well as download
and install grok.

You can also get grok from GitHub::

  git clone git@github.com:zopefoundation/grok.git

Then follow the instructions of ``INSTALL.txt``.
