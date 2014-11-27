Get code blocks from a reStructuredText file using awk
######################################################
:date: 2014-11-27
:tags: bash, awk, rst, metagenomics, sphinx, docutils, workshop
:slug: rst2code
:author: Ino de Bruijn
:summary: Get code blocks from a reStructuredText file using awk

We write most of our metagenomic workshops in `Sphinx
<http://sphinx-doc.org/>`_. Simple `reStructuredText
<http://docutils.sourceforge.net/rst.html>`_ files (``.rst`` files) are
converted into a fancy HTML page. Pretty similar to how this website is
generated actually. We thankfully borrowed this concept from Titus Brown's
`khmer tutorials <http://khmer.readthedocs.org/en/v1.1/>`_. The workshops are
usually done on our computing cluster and consist of a series of bash commands
that each participant has to write in the terminal. One problem we've had with
previous workshops is an easy way to test all these commands. Therefore, for
our latest `metagenomics workshop in Uppsala
<http://metagenomics-workshop.readthedocs.org/en/2014-11-Uppsala/>`_ I wrote a
very simple awk script to get just the code blocks from a ``.rst`` file: 

.. raw:: html

  <script src="https://gist.github.com/inodb/6f571764a6395c9378a0.js"></script>


Code blocks in ``.rst`` are started by a double colon, followed by an indented
code block and ended by an empty line (could contain whitespaces). Once you get
out the code blocks, you can run all the commands by piping it to bash, e.g.

.. code-block:: bash

    cat index.rst | rst2code - | bash -xe

The ``-x`` prints each command before it is run so one can easily detect the
line causing an error and the ``-e`` halts bash in case an error is found.


I am sure there are better ways to do this using ``docutils`` (any tips?), but
for a `hacky test script for the workshop
<https://github.com/EnvGen/metagenomics-workshop/blob/851af9de4fbd1535ae0e13adcd84ed85af859908/test_all.sh>`_
it worked great.
